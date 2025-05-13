from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.messages import get_messages
from django.contrib import messages
from at_system.models import Attendance, Students
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import openpyxl
from django.http import HttpResponse

def attendance_layer(request):
    if request.method == "POST":
        ci = request.POST.get("doc_ci")
        try:
            stundent = Students.objects.get(doc_ci=ci)
            attendance = Attendance(doc_ci=stundent)
            attendance.save()
            messages.success(request, f"Registrado con éxito {stundent.firstname} {stundent.lastname} ✅")
            return HttpResponseRedirect(reverse("attendance_layer"))  # Forzar redirección
        except Students.DoesNotExist:
            messages.error(request, "No está registrado o activo ❌")
            return HttpResponseRedirect(reverse("attendance_layer"))  # Forzar redirección
    return render(request, "asistenciaui.html")

def login_session(request):
    if request.method =="POST":
        user = authenticate(
            request, username = request.POST["usuario"], password = request.POST["password"]   
         )
        if user is None:
             return render(request, "loginUI.html", {'Error': "Contrasenha o Usuario Invalido"})
        else:
            login(request, user)
            return redirect(control_panel)
    else:
        print("no es post")
        
    return render(request, "loginUI.html")
@login_required
def control_panel(request):
    
    return render (request, "control_panelUI.html")

def stundent_register(request):
    if request.method == 'POST':
        fistname = request.get("name")
        lastname = request.get("lastname")
        doc_ci = request.get("doc_ci")
        birthdate = request.get("fecha_nacimiento")
        agg_stds = Students(fistname=fistname, lastname=lastname, doc_ci=doc_ci,date_birthdate=birthdate)
        agg_stds.save()
        messages.success(request, f"Registrado con éxito✅")

    
    return render (request, "student_registration.html")

def attendance_report(request):
    attendance_full = Attendance.objects.filter(date_attendance__isnull=False).order_by('-date_attendance')
    data = []
    for att in attendance_full:
        data.append({
            'ci': att.doc_ci.doc_ci,  
            'student_firstname': att.doc_ci.firstname,
            'student_lastname': att.doc_ci.lastname,
            'date_attendance': att.date_attendance,  
        })
    print(data)
    return render(request,"attendance_reportUI.html", {'data': data})

def logout_sesion(request):
    logout(request)
    return redirect(attendance_layer)

def download_attendance_report(request):
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Informe de Asistencias"


    headers = ["Nombre", "Cédula", "Fecha", "Hora"]
    sheet.append(headers)

    attendance_full = Attendance.objects.filter(date_attendance__isnull=False).order_by('-date_attendance')
    for att in attendance_full:
        sheet.append([
            f"{att.doc_ci.firstname} {att.doc_ci.lastname}",  
            att.doc_ci.doc_ci,  # Cédula
            att.date_attendance.strftime("%d/%m/%Y"),  
            att.date_attendance.strftime("%H:%M"),  
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response['Content-Disposition'] = 'attachment; filename="informe_asistencias.xlsx"'
    workbook.save(response)
    return response