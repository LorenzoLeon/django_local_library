from django import forms

from django.utils.translation import gettext_lazy as _

class SubscribeNewsletter(forms.Form):
    new_email = forms.EmailField(help_text=_("Enter a new email"))  
    new_name = forms.CharField(help_text=_("Enter a new name"))