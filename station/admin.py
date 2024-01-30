from django.contrib import admin
from .models import Station

class StationAdmin (admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']

admin.site.register(Station, StationAdmin)