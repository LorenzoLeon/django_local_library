"""Module providing new dash models."""

from django.db import models
from django.db.models import UniqueConstraint

from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from .behaviors import Authorable, Permalinkable, Timestampable
from .behaviors import Characteristic, TextCharacteristic, NumberCharacteristic


class TerrestrialEcoRegions(models.Model):
    """Class representing a Terrestial Ecoregion WWF"""
    class BiogeographicRealms(models.TextChoices):
        """ENUM representing a Terrestial Realm WWF"""
        NEARCTIC = 'NA', 'Nearctic'
        PALEARCTIC = 'PA', 'Palearctic'
        AFROTROPIC = 'AT', 'Afrotropic'
        INDOMALAYA = 'IM', 'Indomalaya'
        AUSTRALASIA = 'AA', 'Australasia'
        NEOTROPIC = 'NT', 'Neotropic'
        OCEANIA = 'OC', 'Oceania'
        ANTARCTIC = 'AN', 'Antarctic'

    class TerrestrialBiomes(models.TextChoices):
        """ENUM representing a Terrestial Biome WWF"""
        # "Bosques húmedos tropicales y subtropicales"
        TSMF = '1', _(
            'Tropical and subtropical moist broadleaf forests (tropical and subtropical, humid)')
        # "Bosques secos tropicales y subtropicales"
        TSDF = '2', _(
            'Tropical and subtropical dry broadleaf forests (tropical and subtropical, semihumid)')
        # "Bosques de coníferas tropicales y subtropicales"
        TSCF = '3', _(
            'Tropical and subtropical coniferous forests (tropical and subtropical, semihumid)')
        # "Bosques mixtos templados"
        TBMF = '4', _(
            'Temperate broadleaf and mixed forests (temperate, humid)')
        # "Bosques de coníferas templados"
        TCF = '5', _(
            'Temperate coniferous forests (temperate, humid to semihumid)')
        # "Bosque boreal (taiga)"
        TAIGA = '6', _('Boreal forests/taiga (subarctic, humid)')
        # "Matorrales, sabanas y pastizales tropicales y subtropicales"
        TSGSS = '7', _(
            'Tropical and subtropical grasslands, savannas, and shrublands (tropical and subtropical, semiarid)')
        # "Matorrales, sabanas y pastizales templados"
        TGSS = '8', _(
            'Temperate grasslands, savannas, and shrublands (temperate, semiarid)')
        # "Sabanas y pastizales inundables"
        FGS = '9', _(
            'Flooded grasslands and savannas (temperate to tropical, fresh or brackish water inundated)')
        # "Matorrales y pastizales montanos"
        MGS = '10', _(
            'Montane grasslands and shrublands (alpine or montane climate)')
        TUNDRA = '11', _('Tundra (Arctic)')  # "Tundra"
        # "Bosques y matorrales mediterráneos"
        MFWSSF = '12', _(
            'Mediterranean forests, woodlands, and scrub or sclerophyll forests (temperate warm, semihumid to semiarid with winter rainfall)')
        # "Matorrales desérticos y áridos"
        DXS = '13', _(
            'Deserts and xeric shrublands (temperate to tropical, arid)')
        MANGROOVE = '14', _(
            'Mangrove (subtropical and tropical, salt water inundated)')  # "Manglares"
    realm = models.TextField(max_length=2, choices=BiogeographicRealms.choices)
    biome = models.TextField(max_length=2, choices=TerrestrialBiomes.choices)
    id = models.IntegerField(help_text=_("Enter specific biome id"))
    name = models.CharField(max_length=200, unique=True, help_text=_(
        "Enter a Ecoregion (WWF) Name here"))

    def get_code(self):
        """Creates a WWF accepted Ecoregion CODE

        Returns
        -------
            str
        """
        return self.realm+self.biome+self.id


class MarineEcoRegions(models.Model):
    """Class representing a Marine Ecoregion WWF"""
    class BiogeographicRealms(models.TextChoices):
        """ENUM representing a Marine Realm WWF"""
        ARCTIC = '1', _("Arctic")
        TNA = '2', _("Temperate Northern Atlantic")
        TNP = '3', _("Temperate Northern Pacific")
        TRA = '4', _("Tropical Atlantic")
        WIP = '5', _("Western Indo-Pacific")
        CIP = '6', _("Central Indo-Pacific")
        EIP = '7', _("Eastern Indo-Pacific")
        TREP = '8', _("Tropical Eastern Pacific")
        TSA = '9', _("Temperate South America")
        TSAF = '10', _("Temperate Southern Africa")
        TA = '11', _("Temperate Australasia")
        SO = '12', _("Southern Ocean")

    class MarineBiomes(models.TextChoices):
        """ENUM representing a Marine Biome WWF"""
        # "Polar"
        Polar = '1', _("Polar")
        # "Mares y plataformas templadas"
        TSS = '2', _("Temperate shelves and sea")
        # "Surgencias templadas"
        TEU = '3', _("Temperate upwelling")
        # "Surgencias tropicales"
        TRU = '4', _("Tropical upwelling")
        # "Corales tropicales"
        TRC = '5', _("Tropical coral")
    realm = models.TextField(max_length=2, choices=BiogeographicRealms.choices)
    biome = models.TextField(max_length=2, choices=MarineBiomes.choices)
    id = models.IntegerField(help_text=_("Enter specific biome id"))
    name = models.CharField(max_length=200, unique=True, help_text=_(
        "Enter a Ecoregion (WWF) Name here"))

    def get_code(self):
        """Creates a WWF accepted Ecoregion CODE

        Returns
        -------
            str
        """
        return self.realm+self.biome+self.id


class Project(Authorable, Permalinkable):
    """Model representing a Proyect."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Enter a Proyect Name here")
    )
    description = models.TextField(help_text=_(
        "Enter a proyect description"), null=True, blank=True)
    active = models.BooleanField(default=False)
    tags = TaggableManager()

    url_name = "project"

    def __str__(self):
        return str(self.name)

    class Meta:
        """Constraints"""
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='proyect_name_case_insensitive_unique',
                violation_error_message=_(
                    "Proyect already exists (case insensitive match)")
            ),
            UniqueConstraint(
                Lower('slug'),
                name='proyect_slug_case_insensitive_unique',
                violation_error_message=_(
                    "Proyect slug already exists (case insensitive match)")
            ),
        ]


class ProjectTextCharacteristic(Characteristic, TextCharacteristic, Timestampable):
    """Proyect Text Characteristic Model Database"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        """Meta Ordering"""
        ordering = ['modified_date']
        get_latest_by = 'modified_date'


class ProjectNumberCharacteristic(Characteristic, NumberCharacteristic, Timestampable):
    """Proyect Number Characteristic Model Database"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        """Meta Ordering"""
        ordering = ['modified_date']
        get_latest_by = 'modified_date'


class ProjectImage(Timestampable):
    """Proyect Image Model Database"""
    class ImageTypes(models.TextChoices):
        """ENUM representing a Marine Biome WWF"""
        HEAD = 'hi', 'Head Image'
        STOCK = 'st', 'Stock Image'
        EVENT = 'ev', 'Event Image'

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.TextField(max_length=2, choices=ImageTypes.choices)
    file = models.ImageField()

    class Meta:
        """Meta Ordering"""
        ordering = ['modified_date']
        get_latest_by = 'modified_date'

class EventType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Enter an Event Type here")
    )
    file = models.ImageField()


class Event(Authorable, Permalinkable,Timestampable):
    """Model representing a Proyect."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Enter an Event Name here")
    )
    type = models.ForeignKey(EventType, on_delete=models.RESTRICT)
    description = models.TextField(help_text=_(
        "Enter a proyect description"), null=True, blank=True)
    active = models.BooleanField(default=False)
    tags = TaggableManager()

    url_name = "event"

    def __str__(self):
        return str(self.name)

    class Meta:
        """Constraints"""
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='proyect_name_case_insensitive_unique',
                violation_error_message=_(
                    "Proyect already exists (case insensitive match)")
            ),
            UniqueConstraint(
                Lower('slug'),
                name='proyect_slug_case_insensitive_unique',
                violation_error_message=_(
                    "Proyect slug already exists (case insensitive match)")
            ),
        ]


class EventImage(Timestampable):
    """Event Image Model Database"""
    class ImageTypes(models.TextChoices):
        """ENUM representing a Marine Biome WWF"""
        HEAD = 'hi', 'Head Image'
        STOCK = 'st', 'Stock Image'
        EVENT = 'ev', 'Event Image'

    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.TextField(max_length=2, choices=ImageTypes.choices)
    file = models.ImageField()

    class Meta:
        """Meta Ordering"""
        ordering = ['modified_date']
        get_latest_by = 'modified_date'