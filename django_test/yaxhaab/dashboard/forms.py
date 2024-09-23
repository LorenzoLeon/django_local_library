from django import forms
from django.forms import ModelForm

from django.utils.translation import gettext_lazy as _

from .models import MapEvent

class SubscribeNewsletter(forms.Form):
    new_email = forms.EmailField(help_text=_("Enter a new email"))  
    new_name = forms.CharField(help_text=_("Enter a new name"))

class MapEventForm(ModelForm):
    class Meta:
        model= MapEvent
        exclude= ['created_by', 'approved_by_staff','project']

class EventDateForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)