from django.db import models

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse

# Constrains fields to unique values
from django.db.models import UniqueConstraint
# Returns lower cased value of field
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
import uuid # Required for unique book instances


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
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            ),
        ]


class Project(models.Model):
    """Model representing a Proyect."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Enter a Proyect Name here")
    )
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4,
                          help_text=_("Unique ID for this particular book across whole library"))
    credits_issued = models.IntegerField(help_text=_("Enter number of credits issued"))
    credits_sold = models.IntegerField(help_text=_("Enter number of credits sold"))
    money_received = models.IntegerField(help_text=_("Enter number of credits issued"))
    state = models.ForeignKey(State, on_delete=models.RESTRICT, null=False)
    hectares = models.IntegerField(help_text=_("Enter number of hectares in activity area"))
    population = models.IntegerField(help_text=_("Enter community population"))
    land_owners = models.IntegerField(help_text=_("Enter number of land_owners"))
    
    description = models.TextField(help_text=_("Enter a proyect description"),
                                   null=True,
                                   blank=True)

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
                violation_error_message=_("Proyect already exists (case insensitive match)")
            ),
        ]

class MapProject(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Enter a Map Name here")
    )
    TYPE_STATUS = (
        ('v', 'Vector Image'),
        ('a', 'Activity Areas'),
        ('p', 'Points of interest'),
    )
    type = models.CharField(
        max_length=1,
        choices=TYPE_STATUS,
        default='v',
        help_text='Map Type',
    )
    file = models.FileField()
    project = models.ForeignKey(Project, on_delete=models.RESTRICT, null=False)

class PointsOfInterest(models.Model):
    type = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Enter a Point type here")
    )
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('type'),
                name='points_of_interest_type_case_insensitive_unique',
                violation_error_message=_("Points type already exists (case insensitive match)")
            ),
        ]

class MapPoints(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4,
                          help_text=_("Unique ID for this particular map point across whole library"))
    type = models.ForeignKey(PointsOfInterest, on_delete=models.RESTRICT)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    map = models.ForeignKey(MapProject, on_delete=models.RESTRICT)
    size = models.IntegerField(default=1,
                               help_text=_('Size for this Map Point'),
                               max_length=10)

class Event(models.Model):
    type = models.CharField(max_length=200,
                            unique=True,
                            help_text=_("Enter an Event type here"))
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('type'),
                name='event_type_case_insensitive_unique',
                violation_error_message=_("Event type already exists (case insensitive match)")
            ),
        ]

class MapEvents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text=_("Unique ID for this particular map point across whole library"))
    type = models.ForeignKey(Event, on_delete=models.RESTRICT)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    map = models.ForeignKey(MapProject, on_delete=models.RESTRICT)
    description = models.TextField(help_text=_("Enter an event description"), null=True, blank=True)
    link = models.CharField(unique=True,
                            help_text=_("Enter an Event link here"))
    date = models.DateTimeField(help_text=_("Enter the event's date and time"))
    location = 

class MapEventImages(models.Model):
    file = models.ImageField()
    mapevent = models.ForeignKey(MapEvents, on_delete=models.RESTRICT)


