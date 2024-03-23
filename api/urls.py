from django.urls import path
from .views import UserView, PeopleView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('people/', PeopleView.as_view(), name='people'),
]