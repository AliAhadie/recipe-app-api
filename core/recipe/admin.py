from django.contrib import admin
from recipe.models import(Tag,Recipe)

admin.site.register(Tag)
admin.site.register(Recipe)