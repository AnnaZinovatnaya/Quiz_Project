from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all_tests, name='home'),
    path('test/<test_id>/result/', views.show_test_report, name='test_report'),
    path('test/<test_id>/<question_number>/', views.show_question, name='question'),
    path('test/<test_id>/<question_number>/result/', views.check_question, name='question_result'),
    path('test/', views.redirect_to_all_tests),
]