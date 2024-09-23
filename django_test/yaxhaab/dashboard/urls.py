from django.urls import path

from . import views
# Use include() to add paths from the catalog application
from django.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.checkProject, name='project-detail'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/update', views.MapEventUpdateView.as_view(), name='event-update'),
    path('project/<int:pk>/createevent/', views.create_event_user, name='create'),
    path('project2/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail2'),
    path('subscribe', views.subscribe, name='subscribe'),
]

urlpatterns += [
    path('myevents/', views.EventsUserListView.as_view(), name='my-events'),
    path('staffevents/', views.EventsStaffListView.as_view(), name='all-events'),
]

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
