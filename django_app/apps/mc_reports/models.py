from django.db import models
from django.urls import reverse

from ..patients.models import Patient

class MCReport(models.Model):
    origin = models.CharField(max_length=100)
    date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    state_lab = models.CharField(
        choices=[
            ("attached", "Attached"),
            ("not_done", "Not Done")
        ],
        verbose_name="Laboratory test results"
    )
    state_other = models.CharField(
        choices=[
            ("attached", "Attached"),
            ("not_done", "Not Done")
        ],
        verbose_name="Results of other special studies"
    )
    conclusion = models.TextField()
    recommendations = models.TextField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"MC Report #{self.pk}"
    
    def get_absolute_url(self):
        return reverse("mc_reports:mcr-detail", kwargs={"pk": self.pk})