import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.template import loader
import os
import requests
from django.http import JsonResponse
from django.conf import settings
import arrow

def mail_notify(subject, body,  recipients, adjunto):
    sender = "diavlolab@gmail.com"
    password = "nrab zyqd owya gszd"
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ''.join(recipients)
    msg.attach(MIMEText(body,'plain'))
    # if adjunto:
        # with open(adjunto, 'rb') as attachment:
            # part = MIMEBase('aplication', 'octen-steam')
            # part.set_payload(attachment.read())
            # encoders.encode_base64(part)
            # part.add_header('Content-Disposition', f'attachment; filename={}.pdf')
            # msg.attach(part)
    
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp_server:
        smtp_server.login(sender,password)
        smtp_server.sendmail(sender,recipients,msg.as_string())
        print("correo enviado")
        

def normalize_condition(condition):
    print(f"Descripción del clima recibida: {condition}") 
    condition = condition.lower()

    if "sun" in condition:  
        return "Sunny"
    elif "cloud" in condition:  
        return "Cloudy"
    elif "rain" in condition:  
        return "Rainy"
    elif "thunder" in condition or "storm" in condition: 
        return "Thunder"
    else:
        print("No se encontró una palabra clave, devolviendo Unknown")
        return "Unknown"

def get_weather(request):
    date = arrow.now()
    try:
        with open(settings.API_KEY_FILE, 'r') as file:
            api_key = None
            for line in file:
                if line.startswith("apiKey_clima"):
                    api_key = line.split('=')[1].strip().strip("'")  # Extraer la clave
                    break
    except FileNotFoundError:
        return JsonResponse({'error': 'El archivo de API key no fue encontrado'}, status=500)

    if not api_key:
        return JsonResponse({'error': 'API key no configurada o no encontrada en el archivo'}, status=500)

    city = "Limpio"
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    print(f"Ejecutando get_weather...{url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

       
        temperature = data['current']['temp_c']
        humidity = data['current']['humidity']
        condition = data['current']['condition']['text']
        localtime = data['location']['localtime']
        normalized_condition = normalize_condition(condition)  # Normalizar la condición
        print(f"Condición normalizada: {normalized_condition}")

        return JsonResponse({
            'city': city,
            'temperature': temperature,
            'humidity': humidity,
            'condition': normalized_condition,
            'localtime': localtime
        })
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Error al conectar con la API de clima', 'details': str(e)}, status=500)
    except KeyError:
        return JsonResponse({'error': 'Error al procesar los datos de la API'}, status=500)