from modeltranslation.translator import register, TranslationOptions
from .models import Project, Event, MapEvent

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('description')

@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('type')

@register(MapEvent)
class MapEventTranslationOptions(TranslationOptions):
    fields = ('description','title')