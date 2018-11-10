from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tests),
    path('test/<test_id>/', views.test),
    path('test/<test_id>/result/', views.check),
]