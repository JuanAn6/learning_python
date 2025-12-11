import requests
import smtplib
from email.mime.text import MIMEText

def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip")
    except Exception as e:
        return f"Error obteniendo IP externa: {e}"

def send_ip_email(sender_email, sender_password, recipient_email):
    ip = get_external_ip()
    
    # Crear mensaje
    msg = MIMEText(f"La IP externa actual es: {ip}")
    msg['Subject'] = 'IP externa de mi PC'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Conectar al servidor SMTP (Gmail)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Ejemplo de uso
send_ip_email(
    sender_email="tucorreo@gmail.com",
    sender_password="contraseña_de_aplicación",
    recipient_email="destino@gmail.com"
)