from django.contrib import admin
from .models import Track, Coordinates

# Register your models here.
models_list = [Track, Coordinates]
admin.site.register(models_list)