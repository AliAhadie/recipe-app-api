from rest_framework import routers
from .views import (RecipeViewSet,TagApiViewSet)
from django.urls import path,include

app_name='recipe'

router=routers.DefaultRouter()
router.register('recipes',RecipeViewSet)
router.register('tags',TagApiViewSet)

urlpatterns=[
    path('',include(router.urls)),

]