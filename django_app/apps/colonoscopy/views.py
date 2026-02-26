from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from .models import ColonoscopyReport
from .forms import (PassportForm, EvidenceForm, ResultsForm, PhotoProtocolFormSet,
                    InterventionsForm, AdverseEventsForm, ConclusionForm, RecommendationsForm)

@login_required
def colonoscopy_list_view(request):
    context = {
        "app": "colonoscopy",
        "model": "ColonoscopyReport",
        "search_fields": [
            {
                "id": "search__patient__full_name",
                "placeholder": "Patient",
            }, {
                "id": "search__procedure",
                "placeholder": "Procedure",
            }
        ],
        "url_create": "colonoscopy:colonoscopy-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def colonoscopy_detail_view(request, pk):
    try:
        obj = (
            ColonoscopyReport.objects
            .prefetch_related("patient", "photoprotocolimage_set")
            .get(pk=pk)
        )
    except ColonoscopyReport.DoesNotExist:
        raise Http404("Colonoscopy report not found")
    
    context = {
        "app": "colonoscopy",
        "obj": obj,
        "buttons": {
            "back": "colonoscopy:colonoscopy-list",
            "edit": "colonoscopy:colonoscopy-update",
        }
    }
    
    return render(request, "colonoscopy/colonoscopy_detail.html", context)

class ColonoscopyWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ("passport", PassportForm),
        ("evidence", EvidenceForm),
        ("results", ResultsForm),
        ("photoprotocol", PhotoProtocolFormSet),
        ("interventions", InterventionsForm),
        ("adverse_events", AdverseEventsForm),
        ("conclusion", ConclusionForm),
        ("recommendations", RecommendationsForm),
    ]

    templates = {
        "passport": "colonoscopy/colonoscopy_wizard_passport_form.html",
        "evidence": "colonoscopy/colonoscopy_wizard_evidence_form.html",
        "results": "colonoscopy/colonoscopy_wizard_results_form.html",
        "photoprotocol": "colonoscopy/colonoscopy_wizard_photoprotocol_formset.html",
        "interventions": "colonoscopy/colonoscopy_wizard_interventions_form.html",
        "adverse_events": "colonoscopy/colonoscopy_wizard_adverse_events_form.html",
        "conclusion": "colonoscopy/colonoscopy_wizard_conclusion_form.html",
        "recommendations": "colonoscopy/colonoscopy_wizard_recommendations_form.html",
    }

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "colonoscopy_photoprotocol", "0"))

    def get_template_names(self):
        return [ColonoscopyWizardView.templates[self.steps.current]]
    
    def dispatch(self, request, *args, **kwargs):
        # Get the Lab instance.
        pk = self.kwargs.get("pk")
        if pk:
            self.colonoscopy = get_object_or_404(ColonoscopyReport, pk=pk)
        else:
            self.colonoscopy = None

        return super().dispatch(request, *args, **kwargs)
    
    def get_form_instance(self, step):
        return self.colonoscopy
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        context["app"] = "colonoscopy"
        context["url_list"] = "colonoscopy:colonoscopy-list"
        context["url_detail"] = "colonoscopy:colonoscopy-detail"

        return context
    
    def done(self, form_list, form_dict, **kwargs):
        # Save the colonoscopy report
        form = form_dict.get("passport")
        colonoscopy = form.save(commit=False)

        form = form_dict.get("evidence")
        for field, value in form.cleaned_data.items():
            setattr(colonoscopy, field, value)

        form = form_dict.get("results")
        for field, value in form.cleaned_data.items():
            setattr(colonoscopy, field, value)

        form = form_dict.get("interventions")
        for field, value in form.cleaned_data.items():
            setattr(colonoscopy, field, value)

        form = form_dict.get("adverse_events")
        for field, value in form.cleaned_data.items():
            setattr(colonoscopy, field, value)

        form = form_dict.get("conclusion")
        for field, value in form.cleaned_data.items():
            setattr(colonoscopy, field, value)

        form = form_dict.get("recommendations")
        for field, value in form.cleaned_data.items():
            setattr(colonoscopy, field, value)
        
        colonoscopy.save()
        
        # Save the photo protocol images
        formset = form_dict.get("photoprotocol")
        formset.instance = colonoscopy
        formset.save()
        
        return redirect(reverse("colonoscopy:colonoscopy-detail", kwargs = {"pk": colonoscopy.pk}))


def image_append(request):
    if request.method == "POST" and request.headers.get("HX-Request"):
        formset = PhotoProtocolFormSet(prefix="photoprotocol")
        total_forms = request.POST.get("photoprotocol-TOTAL_FORMS")
        context = {
            "total_forms": int(total_forms) + 1,
            "form_id": total_forms,
            "form": formset.empty_form,
        }
        return render(request, "colonoscopy/partials/image_append.html", context)
    else:
        raise Http404("Invalid request")