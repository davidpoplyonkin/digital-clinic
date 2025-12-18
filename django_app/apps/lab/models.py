from django.db import models

from ..patients.models import Patient
from ..tests.models import Test, TestAgeGroup

class Lab(models.Model):
    # It would be intuitive to establish a many-to-one connection with
    # Panel since the latter defines which tests are used in a Lab.
    # However, if, for example, a new test is added to the Panel,
    # Lab will fail to keep up because it also needs a TestResult,
    # which is entered manually. That is why, Lab will be directly
    # connected to TestResult's, and Panel will play the role of
    # a template.

    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    date = models.DateField()
    place = models.CharField(max_length = 100)
    panel = models.CharField(max_length = 100)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Lab #{self.pk}"

class TestResult(models.Model):
    lab = models.ForeignKey(Lab, on_delete = models.CASCADE)
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    value = models.DecimalField(max_digits = 6, decimal_places = 3)
    order = models.PositiveSmallIntegerField()
    cs = models.BooleanField() # clinically significant or not

    class Meta:
        unique_together = ("lab", "test")
        ordering = ["order"]

    def get_reference_values(self):
        """
        Determine the patient's reference values for a given test.
        """
        # Determine the patient's age at the time of laboratory testing.
        patient_age = self.lab.patient.get_age(today_date=self.lab.date)

        age_groups = TestAgeGroup.objects.filter(test=self.test).order_by("max_age")

        for ag in age_groups:
            # If the patient falls into the given age group...
            if patient_age <= ag.max_age:
                return (
                    getattr(ag, f"{self.lab.patient.gender}_min", None),
                    getattr(ag, f"{self.lab.patient.gender}_max", None)
                )
            
        return (None, None)
