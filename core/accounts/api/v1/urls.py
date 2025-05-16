from django.urls import path   
from accounts.api.v1.views import (UserCreateApiView,
                                   AuthTokenApiView,UpdateUserApiView)
 
app_name = 'accounts'

urlpatterns = [
    path('create/',UserCreateApiView.as_view(), name='create'),
    path('token/', AuthTokenApiView.as_view(), name='token'),
    path('me/',UpdateUserApiView.as_view(),name='me')
]