from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('department/', views.DepartmentAPIView.as_view(), name='department-list'),
    path('department/<int:id>/', views.DepartmentAPIView.as_view(), name='department-detail'),
    path('employee/', views.EmployeeAPIView.as_view(), name='employee-list'),
    path('employee/<int:id>/', views.EmployeeAPIView.as_view(), name='employee-detail'),
    path('savefile/', views.SaveFile, name='save-file'),
    path('employee-report/', views.EmployeeReportAPIView.as_view(), name='employee-report'),
]