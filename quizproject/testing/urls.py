from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tests, name='all_tests'),
    path('test/<test_id>/<question_number>/', views.question),
    path('test/<test_id>/<question_number>/result/', views.check),
    path('test/', views.redirect_to_all_tests)
]