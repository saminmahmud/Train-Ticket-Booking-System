from django.contrib import admin
from .models import Train, Seat,Schedule,Review

admin.site.register(Seat)
admin.site.register(Train)
admin.site.register(Schedule)
admin.site.register(Review)