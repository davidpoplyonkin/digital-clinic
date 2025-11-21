from django.db import models
from django.urls import reverse
import datetime

class Patient(models.Model):
    full_name = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="full name"
    )
    gender = models.CharField(
        choices=[
            ("male", "Male"),
            ("female", "Female")
        ],
        verbose_name="gender"
    )
    dob = models.DateField(
        verbose_name="date of birth"
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="height (m)"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="weight (kg)"
    )
    waist_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="waist circumference (cm)"
    )
    phone1 = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="phone 1"
    )
    phone2 = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="phone 2"
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        help_text="Region District City Street Building Apartment",
        verbose_name="address"
    )
    job_title = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="job title"
    )
    disp = models.TextField(
        blank=True,
        verbose_name="dispansery group"
    )
    last_disp = models.DateField(
        blank=True,
        null=True,
        verbose_name="last dispanserisation"
    )
    last_colonoscopy = models.DateField(
        blank=True,
        null=True,
        verbose_name="last colonoscopy"
    )

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("patients:patient-detail", kwargs={"pk": self.pk})
    
    def get_age(self, today_date: datetime.date):
        """
        Calculates a person's age in full years.
        """

        age=today_date.year - self.dob.year

        # If the person's birthday has not yet occured this year, decrement
        # their age.
        if (today_date.month, today_date.day) < (self.dob.month, self.dob.day):
            age -= 1

        return age