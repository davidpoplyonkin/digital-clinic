from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.db.models import Prefetch, Min, Q
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (LabWizardLabForm, LabWizardResForm, LabWizardResFormSet,
                    LabWizardResStep)
from .models import Lab, TestResult
from ..tests.models import Test

try:
    from .utils.lab_pdf_generator import generate_pdf
except ModuleNotFoundError:
    from ..core.utils.example_pdf_generator import generate_pdf

@login_required
def lab_list_view(request):

    context = {
        "app": "lab",
        "model": "Lab",
        "search_id": "search__patient__full_name",
        "search_placeholder": "Patient Name",
        "url_create": "lab:lab-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def lab_detail_view(request, pk):
    lab = get_object_or_404(Lab, pk = pk)
    res = (
        TestResult.objects
        .filter(lab = lab)
        .select_related("test")
    )
    
    context = {
        "app": "lab",
        "obj": lab,
        "res": res,
        "buttons": {
            "back": "lab:lab-list",
            "edit": "lab:lab-update",
            "print": "lab:lab-print",
            "delete": "lab:lab-delete",
        }
    }
    
    return render(request, "lab/lab_detail.html", context)

class LabWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ("lab", LabWizardLabForm),
        ("res", LabWizardResStep)
    ]

    templates = {
        "lab": "lab/lab_wizard_lab_form.html",
        "res": "lab/lab_wizard_res_form.html"
    }

    def get_template_names(self):
        return [LabWizardView.templates[self.steps.current]]
    
    def dispatch(self, request, *args, **kwargs):

        # Get the Lab instance.
        pk = self.kwargs.get("pk")
        if pk:
            self.lab = get_object_or_404(Lab, pk=pk)
        else:
            self.lab = None

        return super().dispatch(request, *args, **kwargs)
    
    def _update_lab(self, step):
        if step == "res":
            # Update the Lab instance with the data from the first step.
            prev_data = self.get_cleaned_data_for_step("lab")

            if self.lab is None:
                self.lab = Lab(**prev_data)
            else:
                for attr_name, attr_value in prev_data.items():
                    setattr(self.lab, attr_name, attr_value)
    
    def get_form_instance(self, step):
        instance = super().get_form_instance(step)

        if step == "lab":
            return self.lab

        return instance
    
    def get_form(self, step=None, data=None, files=None):

        if step is None:
            step = self.steps.current
        
        if step == "res":
            self._update_lab(step)

            # Prefill the form with data from the previous step.
            form = LabWizardResForm(data, instance=self.lab)
            formset = LabWizardResFormSet(data, instance=self.lab)
            
            return LabWizardResStep(form, formset)
        
        return super().get_form(step, data, files)
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        context["app"] = "lab"
        
        if self.steps.current == "res":
            # Prepare context for the template.
            context["form"] = form.form
            context["formset"] = form.formset

            if self.lab.pk:
                context["panel_on_load_post"] = reverse(
                    "lab:lab-update-testresult-update", kwargs={"pk": self.lab.pk})
            else:
                context["panel_on_load_post"] = reverse(
                    "lab:lab-create-testresult-update")

        return context
    
    def process_step(self, form):
        if self.steps.current == "res":
            # Both the form and the formset are created using all data from the
            # request. So, form.form.data and form.formset.data are essentially
            # duplicates, and it is sufficient to return only one of them.

            return form.form.data
        
        return super().process_step(form)
    
    def done(self, form_list, **kwargs):
        lab = form_list[1].save()

        return redirect(reverse("lab:lab-detail", kwargs = {"pk": lab.pk}))
    
    def _testresult_update(self):
        form_data = self.request.POST
        context = {
            "results": [],
            "on_input_post": form_data.get("panel_on_load_post"),
        }

        if form_data.get("panel_initial_render"):
            # In other words, this is the first time this function is triggered for
            # the given form, and this happens immediately after the form is
            # rendered. In this case, the panel name is guaranteed to be the same
            # as when the wizard retrieved the test results, and therefore there is
            # no need to update them.

            context["initial_render"] = True
            return render(self.request, "lab/partials/testresult_update.html", context)
        
        self._update_lab("res")

        required_tests = (
            Test.objects

            # Annotate each Test with the minimum order of its related
            # PanelTest's that are also connected to the current Panel
            # (given that each combination of Test and Panel is unique,
            # there will be no more than one related PanelTest instance, and
            # Min will be equal to the order of such instance or NULL if it
            # doesn't exist)
            .annotate(order=Min(
                "paneltest__order",
                filter=Q(paneltest__panel__name=form_data.get("panel"))
            ))

            # Exclude the Test's that are not connected to the current
            # Panel.
            .exclude(order__isnull=True)

            # Prefetch the related TestResult's that are also connected to
            # the current Lab. 
            .prefetch_related(Prefetch(
                "testresult_set",
                queryset=TestResult.objects.filter(lab__pk=self.lab.pk),
                to_attr="results"
            ))

            # Use the annotated order field to sort the Test's
            .order_by("order")
        )

        # It seems that Django expects the old forms - those corresponding to
        # existing objects - to have prefix indices in the range from 0 to
        # INITIAL_FORMS - 1, and the new forms to have larger indices.
        # Therefore, the index of the first new form will be equal to the
        # number of TestResult's currently connected to the lab.
        old_form_prefix_idx = 0
        if self.lab.pk:
            new_form_prefix_idx = self.lab.testresult_set.count()
        else:
            new_form_prefix_idx = 0

        for i, t in enumerate(required_tests, start=1):
            if t.results:
                # If there is an existing TestResult, take it.
                test_res = t.results[0]
                prefix_idx = old_form_prefix_idx
                old_form_prefix_idx += 1
            else:
                # Otherwise, create one.
                test_res = TestResult(test=t)
                prefix_idx = new_form_prefix_idx
                new_form_prefix_idx += 1

            test_res.lab = self.lab
            test_res.order = i

            context["results"].append({
                "tr": test_res,
                "prefix": f"testresult_set-{prefix_idx}",
            })

        if not context["results"]:
            context["no_matching_panel"] = True

        # The TestResult's that are connected to the current Lab but are not
        # required for the current Panel need to be deleted.
        redundant_results = (
            TestResult.objects
            .filter(lab__pk=self.lab.pk)
            .exclude(test__in=required_tests)
        )

        for i, r in enumerate(
            redundant_results,
            start=(len(context["results"]) + 1)
        ):
            r.lab = self.lab
            context["results"].append({
                "tr": r,
                "prefix": f"testresult_set-{old_form_prefix_idx}",
                "del": True
            })
            old_form_prefix_idx += 1

        return render(self.request, "lab/partials/testresult_update.html", context)
        
    def post(self, *args, **kwargs):       
        # Catching the requests to update the test results in response to a
        # change in the panel name. Currently, thes are the only HTMX requests
        # the wizard handles.
        if self.request.headers.get("HX-Request") and self.steps.current == "res":
            return self._testresult_update()

        return super().post(*args, **kwargs)

@login_required
def lab_delete_view(request, pk):

    obj = get_object_or_404(Lab, pk=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("lab:lab-list")
    
    context = {
        "app": "lab",
        "title": "Lab",
        "obj": obj,
        "url_detail": "lab:lab-detail",
    }

    return render(request, "digital_clinic/delete_view.html", context)

@login_required
def lab_print(request, pk):
    try:
        obj = (
            Lab.objects
            .prefetch_related("patient", "testresult_set__test")
            .get(pk=pk)
        )
    except Lab.DoesNotExist:
        raise Http404("Lab object not found")

    response = HttpResponse(generate_pdf(obj), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=lab.pdf"

    return response
