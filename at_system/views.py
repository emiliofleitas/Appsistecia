from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from at_system.models import Attendance, Students
from django.contrib.auth.decorators import login_required


def attendance_layer(request):
    if request.method == "POST":
        ci = request.POST.get("doc_ci")
        try:
            stundent = Students.objects.get(doc_ci = ci)
            if stundent:
                attendance = Attendance(doc_ci = stundent)
                attendance.save()
                messages.success(request, f"Registrado con éxito {stundent.fistname }{stundent.lastname} ✅")
            return redirect("attendance_layer")
        except Students.DoesNotExist:
            messages.error(request, "No está registrado o activo ❌")
            return redirect("attendance_layer") 
    else:
        print("no es un metodo post")
        
    return render(request,"asistenciaui.html", {'success':"Registrado con exito ✅"})

# Create your views here.
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
        birthdate = request.get("date")
        agg_stds = Students(fistname=fistname, lastname=lastname, doc_ci=doc_ci,birthdate=birthdate)
        agg_stds.save()
        messages.success(request, f"Registrado con éxito✅")

    
    return render (request, "student_registration.html")

def attendance_report(request):
    return render(request,"attendance_reportUI.htmt;")

def logout_sesion(request):
    logout(request)
    return redirect(attendance_layer)