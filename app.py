from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', '123')

# Variables de entorno que debes configurar en Render
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')  # tu correo verificado en SendGrid
TO_EMAIL = os.getenv('TO_EMAIL')      # correo donde quieres recibir los mensajes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        # Crear el mensaje usando SendGrid
        msg = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject='Nuevo mensaje de contacto',
            plain_text_content=f"Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}"
        )

        # Enviar el mensaje
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(msg)

        print(f"Correo enviado, status code: {response.status_code}")
        flash("Mensaje enviado correctamente.", "success")

    except Exception as e:
        print(f"Error: {e}")
        flash("Ocurrió un error al enviar el mensaje. Intenta de nuevo más tarde.", "danger")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
