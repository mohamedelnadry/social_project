
from django.urls import path
from .views import Register,Create, UserView,Refresh, Revoke


urlpatterns = [
    path('register/', Register.as_view(),name='register'),
    path('create/', Create.as_view(),name='create'),
    path('refresh/', Refresh.as_view(),name='refresh'),
    path('revoke/', Revoke.as_view(),name='revoke'),
    path('user/', UserView.as_view(),name='userview'),



]
