from django.shortcuts import render,redirect

from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from dashboard.forms import SubscribeNewsletter
from django.contrib.auth.models import User
from django.views import generic
from django.db.models import Sum
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Project, MapEvent,SubscribedUser,MapEventImage,MapEventSerializer
from .forms import MapEventForm,EventDateForm

from django.urls import reverse

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_projects = Project.objects.all().count()
    num_mapevents = MapEvent.objects.all().count()
    num_hectares = Project.objects.all().aggregate(Sum("hectares"))
    num_hectares = round(num_hectares["hectares__sum"], -3)

    # Available books (status = 'a')
    num_active_projects = Project.objects.filter(active=True).count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_projects': num_projects,
        'num_mapevents': num_mapevents,
        'num_active_projects': num_active_projects,
        'num_visits': num_visits,
        'num_hectares': num_hectares,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeNewsletter(request.POST)
        if form.is_valid():
            semail = form.cleaned_data['new_email']
            sname = form.cleaned_data['new_email']
            subscribe_user = SubscribedUser.objects.filter(email=semail).first()
            if subscribe_user:
                messages.error(request, _('%(email)s email address is already a subscriber') % {'email': semail})
            else:
                subscribe_model_instance = SubscribedUser()
                subscribe_model_instance.name = sname
                subscribe_model_instance.email = semail
                subscribe_model_instance.save()
                messages.success(request, _('%(email)s email was successfully subscribed to our newsletter!') % {'email': semail})
        else:
            messages.error(request, _("You must type legit name and email to subscribe to a Newsletter"))
        return redirect('{}#signup'.format(reverse('index')))
    
class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 5
    
class ProjectDetailView(generic.DetailView):
    model = Project
    
class EventsUserListView(LoginRequiredMixin,generic.ListView):
    model = MapEvent
    login_url = "/dashboard/accounts/login"
    def get_queryset(self):
        return (
            MapEvent.objects.filter(created_by=self.request.user)
            .order_by('date')
        )

#@staff_member_required
class EventsStaffListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'dashboard.can_mark_approved'
    login_url = "/dashboard/accounts/login"
    model = MapEvent

class EventDetailView(generic.DetailView):
    model = MapEvent

import datetime

@login_required
def create_event_user(request, pk):
    project = get_object_or_404(Project, pk=pk)
    image_form_set = modelformset_factory(MapEventImage,exclude=['created_by','mapevent' ], extra=2)

    if request.method == 'POST':

        event_form = MapEventForm(request.POST)
        event_form.project = project
        formset = image_form_set(request.POST, request.FILES,
                               queryset=MapEventImage.objects.none())


        if event_form.is_valid() and formset.is_valid():
            event = event_form.save(commit=False)
            event.created_by = User.objects.get(user = request.user)
            event.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = MapEventImage(mapevent=event, file=image)
                photo.save()
            messages.success(request,"Posted!")
            return redirect(event.get_absolute_url())
        else:
            print( event_form.errors, formset.errors)
    else:
        event_form = MapEventForm(initial={'date':datetime.date.today()})
        formset = image_form_set(queryset=MapEventImage.objects.none())

    context={
        'project': project,
        'event_form': event_form, 
        'formset': formset
    }
    return render(request,'create_event.html',context)


def checkProject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    events = MapEvent.objects.filter(project = project)
    mindate = events.earliest('date').date
    maxdate = events.latest('date').date

    if request.method == 'POST':
        event_date_form = EventDateForm(request.POST)
        if event_date_form.is_valid():
            mindate = event_date_form.cleaned_data['mindate']
            maxdate = event_date_form.cleaned_data['maxdate']
            events = MapEvent.objects.filter(project = project).filter(date__range=[mindate, maxdate])
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                #AJAX Request
                ser_events = [ev.as_dict() for ev in events]
                return JsonResponse({'events': ser_events})
            messages.success(request,"Query!")
        else:
            print(event_date_form.errors)
    else:
        event_date_form = EventDateForm(initial={'mindate':mindate,'maxdate':maxdate})
    context={
        'project': project,
        'event_date_form': event_date_form,
        'events': events,
    }
    return render(request,'check_project_event.html',context)