from django.urls import path

from . import views
# Use include() to add paths from the catalog application
from django.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
]

urlpatterns += [
    path('subscribe', views.subscribe, name='subscribe'),
]
urlpatterns += [
    path('project/<int:pk>/createevent/', views.create_event_user, name='create'),
    path('project2/<int:pk>/', views.checkProject, name='project-detail2'),
]
urlpatterns += [
    path('myevents/', views.EventsUserListView.as_view(), name='my-events'),
]

urlpatterns += [
    path('staffevents/', views.EventsStaffListView.as_view(), name='all-events'),
]

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
