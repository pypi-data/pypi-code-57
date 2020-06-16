from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.db import models
from .models import Event

admin.site.register(Event, GuardedModelAdmin)
    
