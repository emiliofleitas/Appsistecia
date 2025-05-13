from django.db import models
from django.contrib.auth.models import User


class Students(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    doc_ci = models.DecimalField(max_digits=15, decimal_places=0)
    date_register = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now_add=True)
    date_birthdate = models.DateField(verbose_name="fecha_nacimiento", null=False, blank=False)
    agg = models.ForeignKey(User, on_delete=models.CASCADE)


class Attendance(models.Model):
    doc_ci = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, related_name='ci_student')
    date_attendance = models.DateTimeField(auto_now_add=True)
    
    