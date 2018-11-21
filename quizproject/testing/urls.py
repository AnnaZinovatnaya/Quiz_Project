from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tests, name='home'),
    path('test/<test_id>/<question_number>/', views.question, name='question'),
    path('test/<test_id>/<question_number>/result/', views.check, name='question_result'),
    path('test/', views.redirect_to_all_tests)
]