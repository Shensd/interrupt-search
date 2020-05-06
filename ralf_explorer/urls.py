from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.view_filtered_interrupts, name='filter'),
    path('filter/json/', views.view_filtered_json, name='filter_json'),
    path('info/', views.view_info, name='view_info')
]