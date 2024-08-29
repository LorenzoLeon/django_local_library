from django.db import models
from django.contrib.auth.models import User
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
    abr = models.CharField(max_length=3, unique=True, help_text=_('Enter 3 characters as project abbreviation'))
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
    active = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular proyect instance."""
        return reverse('project-detail', args=[str(self.id)])

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

    def __str__(self):
        """String for representing the Model object."""
        return self.type
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('type'),
                name='points_of_interest_type_case_insensitive_unique',
                violation_error_message=_("Points type already exists (case insensitive match)")
            ),
        ]

class PointsInstance(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4,
                          help_text=_("Unique ID for this particular map point across whole library"))
    type = models.ForeignKey(PointsOfInterest, on_delete=models.RESTRICT)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    map = models.ForeignKey(MapProject, on_delete=models.RESTRICT)
    size = models.IntegerField(default=1,
                               help_text=_('Size for this Map Point'))
    loc_x = models.FloatField()
    loc_y = models.FloatField()

class Event(models.Model):
    type = models.CharField(max_length=200,
                            unique=True,
                            help_text=_("Enter an Event type here"))
    imgbackground = models.ImageField(upload_to='images/')

    def __str__(self):
        """String for representing the event."""
        return self.type
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('type'),
                name='event_type_case_insensitive_unique',
                violation_error_message=_("Event type already exists (case insensitive match)")
            ),
        ]

"""Don't forget LoginRequiredMixin in map event creation view"""
class MapEvent(models.Model):
    title = models.CharField(max_length=200,
                             unique=True,
                             help_text=_("Enter an Event link here"))
    type = models.ForeignKey(Event, on_delete=models.RESTRICT)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    description = models.TextField(help_text=_("Enter an event description"), null=True, blank=True)
    link = models.CharField(max_length=200,
                            unique=True,
                            help_text=_("Enter an Event link here"))
    date = models.DateTimeField(help_text=_("Enter the event's date and time"))
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    loc_x = models.FloatField()
    loc_y = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('event-detail', args=[str(self.id)])

class MapEventImage(models.Model):
    title = models.CharField(max_length=200,
                             help_text=_("Enter an image title here"))
    description = models.TextField(help_text=_("Enter an image description here"))
    file = models.ImageField()
    mapevent = models.ForeignKey(MapEvent, on_delete=models.RESTRICT)

from django.utils import timezone

class SubscribedUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,primary_key=True, unique=True,help_text=_("Email address for newsletter signup"))
    added_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email