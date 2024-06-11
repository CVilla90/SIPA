# Portfolio/SIPA/courses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data_science/', views.data_science, name='data_science'),
    path('filter_courses/', views.filter_courses, name='filter_courses'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_competency/', views.add_competency, name='add_competency'),
]
