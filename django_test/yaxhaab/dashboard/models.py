from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse

# Constrains fields to unique values
from django.db.models import UniqueConstraint
# Returns lower cased value of field
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _


class State(models.Model):
    """Model representing a federal state."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a federal entity"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('language-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            ),
        ]


class Proyect(models.Model):
    """Model representing a Proyect."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Enter a Proyect Name here")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    credits_issued = models.IntegerField(
        help_text=_("Enter number of credits issued"))
    credits_sold = models.IntegerField(
        help_text=_("Enter number of credits sold"))
    money_received = models.IntegerField(
        help_text=_("Enter number of credits issued"))
    state = models.ForeignKey(State, on_delete=models.RESTRICT, null=True)
    hectares = models.IntegerField(help_text=_(
        "Enter number of hectares in activity area"))
    population = models.IntegerField(help_text=_("Enter community population"))
    land_owners = models.IntegerField(
        help_text=_("Enter number of land_owners"))
    
    description = models.TextField(help_text="Enter a proyect description", null=True, blank=True)

    def get_abr(self):
        return [s[0] for s in self.name.split()].join().upper()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular proyect instance."""
        return reverse('proyect-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='proyect_name_case_insensitive_unique',
                violation_error_message="Proyect already exists (case insensitive match)"
            ),
        ]