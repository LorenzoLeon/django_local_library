from django.shortcuts import render,redirect

from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from dashboard.forms import SubscribeNewsletter
from django.views import generic
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Project, MapEvent,SubscribedUser


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