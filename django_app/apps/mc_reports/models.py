from django.db import models

from ..patients.models import Patient

class MCReport(models.Model):
    origin = models.CharField(max_length=100)
    date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    state_lab = models.CharField(
        choices=[
            ("attached", "Attached"),
            ("not_done", "Not Done")
        ]
    )
    state_other = models.CharField(
        choices=[
            ("attached", "Attached"),
            ("not_done", "Not Done")
        ]
    )
    conclusion = models.CharField(max_length=1000)
    recommendations = models.CharField(max_length=1000)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"MC Report #{self.pk}"