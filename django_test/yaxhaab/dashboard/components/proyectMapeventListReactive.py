from datetime import date
from django_unicorn.components import UnicornView, QuerySetType
from django.shortcuts import get_object_or_404

from dashboard.models import Project, MapEvent

class ProyectmapeventlistreactiveView(UnicornView):
    project: Project = None
    mapevents: QuerySetType[MapEvent] = MapEvent.objects.none()
    initdate = date.today()
    enddate = date.today()

    def mount(self):
        self.project = get_object_or_404(Project,id = self.component_kwargs["projectpk"])
        self.mapevents = MapEvent.objects.filter(project = self.project)
        self.initdate = self.mapevents.earliest('date').date
        self.enddate = self.mapevents.latest('date').date

    def load_table(self):
        self.mapevents = MapEvent.objects.filter(project = self.project)

    def updated_initdate(self, query):
        self.load_table()
        self.mapevents = self.mapevents.filter(date__range=[query, self.enddate])

    def updated_enddate(self, query):
        self.load_table()
        self.mapevents = self.mapevents.filter(date__range=[self.initdate, query])