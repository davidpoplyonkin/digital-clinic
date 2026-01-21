from django.db import models

from ..patients.models import Patient

class XRaysExamination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    examination = models.CharField(max_length=200)
    date = models.DateField()
    medical_record_number = models.CharField(max_length=20, blank=True)
    technical_parameters = models.TextField()
    description = models.TextField()
    conclusion = models.TextField()
    recommendations = models.TextField()
    doctor_name = models.CharField(max_length=30)
