from django.contrib import admin

# Register your models here.
from .models import State, Project, Event, PointsInstance, MapEvent, MapEventImage, MapProject, PointsOfInterest, SubscribedUser


admin.site.register(State)
admin.site.register(Event)
admin.site.register(PointsOfInterest)

@admin.register(SubscribedUser)
class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'added_date')

class MapEventInline(admin.TabularInline):
    model = MapEvent
    extra = 0
    
class PointsInstanceInline(admin.TabularInline):
    model = PointsInstance
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'abr', 'credits_issued',
                    'land_owners', 'active')

    fieldsets = (
        (None, {'fields': ('name','abr', 'description', 'state','active')}),
        ('CRTs', {'fields': ('credits_issued','credits_sold','money_received')}),
        ('Context',{'fields': ('hectares','land_owners','population')})
    )
    inlines = [MapEventInline]


class MapEventImagesInline(admin.TabularInline):
    model = MapEventImage
    extra = 0

@admin.register(MapEvent)
class MapEventAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'type', 'created_by')
    list_filter = ('project', 'date')

    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'created_by')
        }),
        ('Description', {
            'fields': ('type', 'description', 'date', 'loc_x', 'loc_y')
        }),
    )
    inlines = [MapEventImagesInline]