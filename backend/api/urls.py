from django.urls import path
from . import views

urlpatterns = [
    path('updates/', views.check_for_updates, name="check-for-updates"),
    path('update/', views.update_system, name="update_system")
]
