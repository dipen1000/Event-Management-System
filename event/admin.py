from django.contrib import admin
from event.models import *

class EventInline(admin.TabularInline):
    model = Event
    readonly_fields = ('id',)
    
@admin.register(EventCategory)    
class EventCategory(admin.ModelAdmin):
    list_display = [
        'id', 'event_name'
    ]
    ordering = ('id',)
    search_fields = ('event_name',)
    list_per_page = 10
    
    inlines = [
        EventInline
    ]
    
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'email', 'address', 'phone'
    ]
    ordering = ('id',)
    search_fields = ('name',)

@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'address', 'phone'
    ]    
    ordering = ('id',)
    search_fields = ('name',)
    
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'address', 'phone', 'event'
    ]
    ordering = ('id',)
    search_fields = ('name', 'event',)
    
@admin.register(EventLogistics)
class EventLogisticsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'event', 'catering', 'get_equipments', 'transportation'
    ]
    ordering = ('id',)
    search_fields = ('event__name',)
    
    def get_equipments(self, obj):
        return ", ".join(equipment.name for equipment in obj.equipments.all())  
    
    get_equipments.short_description = 'Equipments'
    
admin.site.register(Ticket)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Reservation)