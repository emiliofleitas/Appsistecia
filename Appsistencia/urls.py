"""
URL configuration for Appsistencia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from at_system import views
from at_system.views import download_attendance_report

urlpatterns = [
    path('admin', admin.site.urls),
    path('', lambda request: redirect('attendance_layer', permanent=False)),
    path('attendance/', views.attendance_layer, name="attendance_layer"),
    path('login_session/',views.login_session, name="login_session"),
    path('logout_sesion/',views.logout_sesion, name="logout_sesion"),
    path('control_panel',views.control_panel, name="control_panel"),
    path('student_registration/',views.stundent_register, name="student_registration"),
    path('attendance_report',views.attendance_report, name="attendance_report"),
    path('download_attendance_report/', download_attendance_report, name="download_attendance_report"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)