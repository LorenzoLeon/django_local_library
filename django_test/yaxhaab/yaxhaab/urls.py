from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    path('', RedirectView.as_view(url='dashboard/', permanent=True)),
# Use static() to add URL mapping to serve static files during development (only)
    #static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)