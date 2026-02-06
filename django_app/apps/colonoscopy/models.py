from django.db import models
from multiselectfield import MultiSelectField
from pathlib import Path
import uuid

from ..patients.models import Patient

class ColonoscopyReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    organisation = models.CharField(max_length=100)
    colonoscopist = models.CharField(max_length=50)
    colonoscopist_phone = models.CharField(max_length=50)
    procedure = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField(blank=True)

    doctor = models.CharField(max_length=50)
    doctor_phone = models.CharField(max_length=50)

    diagnosis = models.TextField()
    evidence = models.TextField()

    asa_classification = models.CharField(
        choices=[
            ("1", "Class I"),
            ("2", "Class II"),
            ("3", "Class III"),
            ("4", "Class IV")
        ],
        verbose_name = "ASA classification"
    )
    sedation = models.CharField(
        choices=[ 
            ("no_sedation", "No sedation"),
            ("conscious_sedation", "Conscious sedation"),
            ("deep_sedation", "Deep sedation"),
            ("general_anesthesia", "General anesthesia")
        ]
    )
    anesthetist = models.CharField(max_length=50)

    bowel_prep = models.CharField(
        choices=[
            ("excellent", "Excellent"),
            ("good", "Good"),
            ("satisfactory", "Satisfactory"),
            ("insufficient", "Insufficient"),
        ],
        verbose_name="Bowel preparation"
    )
    bbps = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Boston bowel preparation score"
    )
    insertion_level = models.CharField(
        choices=[
            ("ti", "Terminal ileum"),
            ("c", "Caecum"),
            ("ac", "Ascending colon"),
            ("hf", "Hepatic flexure"),
            ("tc", "Transverse colon"),
            ("sf", "Splenic flexure"),
            ("dc", "Descending colon"),
            ("sc", "Sigmoid colon"),
            ("r", "Rectum"),
        ]
    )
    visualization = MultiSelectField(
        choices=[
            ("iv", "Ileocaecal valve"),
            ("tcf", "Tripartite caecal folds"),
            ("ao", "Appendiceal orifice"),
            ("ti", "Terminal ileum"),
            ("a", "Anastomosis"),
        ]
    )
    biopsy_referral = models.PositiveSmallIntegerField()
    withdrawal_time = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )

    finger_examination = models.TextField()
    ileum = models.TextField()
    right_colon = models.TextField()
    colon_transversum = models.TextField()
    colon_descendens = models.TextField()
    sigmoid = models.TextField()
    rectum = models.TextField()

    adversary_events = models.TextField(blank=True)
    conclusion = models.TextField()

    next_colonoscopy = models.CharField(
        choices=[
            ("4y", "NBCSP через 4 роки"),
            ("2y", "Lynch syndrome - repeat colonoscopy after 2 years"),
            ("0y", "Once confirmed, pathology will schedule the next colonoscopy."),
        ]
    )
    follow_up_with = models.CharField(
        choices=[
            ("gp", "General practitioner"),
            ("spec", "Specialist")
        ]
    )
    recommendations = models.TextField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Colonoscopy Report #{self.pk}"

class PhotoProtocolImage(models.Model):
    def get_upload_path(instance, filename):
        extension = Path(filename).suffix # .jpg, .png
        new_filename = f"{uuid.uuid4()}{extension}"

        return Path("colonoscopy_photoprotocol") / str(instance.colonoscopy.pk) / new_filename
    
    colonoscopy = models.ForeignKey(ColonoscopyReport, on_delete=models.CASCADE)
    image = models.ImageField()
    caption = models.CharField(max_length=200)
