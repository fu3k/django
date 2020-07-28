################################################################################################
#webapp
---------techie/admin.py-----------------------------
from django.contrib import admin
from .models import Destination
# Register your models here.
admin.site.register(Destination)

---------techie/apps.py---------------------------------
from django.apps import AppConfig


class TechieConfig(AppConfig):
    name = 'techie'

################################################################################################
# mysite
---------polls/admin.py-----------------------------
from django.contrib import admin
from .models import Question

admin.site.register(Question)

---------polls/apps.py---------------------------------
''' nothing''''

################################################################################################
# 