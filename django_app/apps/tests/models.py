from django.db import models

class Test(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    units = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if self.units:
            return f"{self.name} ({self.units})"   
        else:
            return f"{self.name}"
    
class TestAgeGroup(models.Model):
    """
    After the age groups are sorted in ascending order by the `max_age`
    field, they should be interpreted as follows: if the patient's age
    is between the previous age group `max_age` exclusive and this
    age group `max_age` inclusive, the patient should normally score
    between min and max on the `test`.
    """

    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    max_age = models.PositiveSmallIntegerField()

    male_min = models.DecimalField(
        max_digits = 6,
        decimal_places = 3,
    )
    male_max = models.DecimalField(
        max_digits = 6,
        decimal_places = 3,
    )
    female_min = models.DecimalField(
        max_digits = 6,
        decimal_places = 3,
    )
    female_max = models.DecimalField(
        max_digits = 6,
        decimal_places = 3,
    )

    class Meta:
        ordering = ["max_age"]