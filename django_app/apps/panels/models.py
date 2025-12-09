from django.db import models

from ..tests.models import Test

class Panel(models.Model):
    """
    A collection of tests.
    """

    name = models.CharField(
        max_length = 100,
        unique = True
    )
    tests = models.ManyToManyField(Test, through = "PanelTest")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class PanelTest(models.Model):
    """
    A junction table between Panels and Tests.
    """

    panel = models.ForeignKey(Panel, on_delete = models.CASCADE)
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("panel", "test")
        ordering = ["order"]
