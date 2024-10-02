from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Permalinkable(models.Model):
    slug = models.SlugField(unique=True, default="", null=False)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(self.url_name, args=(self.slug))


class Publishable(models.Model):
    publish_date = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def publish_on(self, date=None):
        if not date:
            date = timezone.now()
        self.publish_date = date
        self.save()

    @property
    def is_published(self):
        return self.publish_date and self.publish_date < timezone.now()


class Aprovable(models.Model):
    approved = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Authorable(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Characteristic(models.Model):
    name = models.CharField(max_length=50, help_text=_(
        "Enter a characteristic title here"))

    class Meta:
        abstract = True


class TextCharacteristic(models.Model):
    text = models.TextField(help_text=_("Enter the characteristic description"))
    class Meta:
        abstract = True


class NumberCharacteristic(models.Model):
    value = models.FloatField(help_text=_("Enter the characteristic value"))
    class Meta:
        abstract = True


class FreshwaterBiomes(models.TextChoices):
    LAKES   = '1', _('Large lakes') #"Grandes lagos"
    DELTAS  = '2', _('Large river deltas') #"Grandes deltas de ríos"
    POLAR   = '3', _('Polar freshwaters') #"Agua dulce polar"
    MONT    = '4', _('Montane freshwaters') #"Agua dulce montana"
    TCR     = '5', _('Temperate coastal rivers') #"Ríos costeros templados"
    TFRW    = '6', _('Temperate floodplain rivers and wetlands') #"Humedales y ríos de planicies templadas"
    TUR     = '7', _('Temperate upland rivers') #"Ríos de montaña templados"
    TSCR    = '8', _('Tropical and subtropical coastal rivers') #"Ribereño"
    TSFRW   = '9', _('Tropical and subtropical floodplain rivers and wetlands') #"Humedales y ríos de planicies tropicales y subtropicales"
    TSUR    = '10', _('Tropical and subtropical upland rivers') #"Ríos de montaña tropicales y subtropicales"
    XFEB    = '11', _('Xeric freshwaters and endorheic basins') #"Cuencas endorreicas y aguadulce en zonas áridas"
    ISLAND  = '12', _('Oceanic islands') #"Islas oceánicas"