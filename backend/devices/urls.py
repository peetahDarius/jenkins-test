from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreateDeviceView.as_view(), name="create-view-devices"),
    path("<int:pk>", views.RetrieveUpdateDeleteDeviceView.as_view(), name="retrieve-update-delete-device")
]
