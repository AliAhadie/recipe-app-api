from django.urls import path   
from accounts.api.v1.views import UserCreateApiView
 
app_name = 'accounts'

urlpatterns = [
    path('create/',UserCreateApiView.as_view(), name='create'),
]