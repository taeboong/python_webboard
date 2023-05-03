from django.urls.conf import path

from board import views

urlpatterns = [
    path('', views.index, name='list'),
    path('write_form/', views.write_form, name='write_form'),
    path('write/', views.write, name='write'),
    path('view/<int:bData_id>/', views.view, name='view'),
    path('modify_form/<int:bData_id>/', views.modify_form, name='modify_form'),
    path('modify/<int:bData_id>/', views.modify, name='modify'),
    path('delete/<int:bData_id>/', views.delete, name='delete'),
]