from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY', '123')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')  # tu correo verificado en SendGrid
TO_EMAIL = os.getenv('TO_EMAIL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        #Crear el mensaje de correo

        msg = Message('Nuevo mensaje de contacto',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}"

        #enviar el mensaje
        mail.send(msg)
        flash("Mensaje enviado correctamente.", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash("Ocurrió un error al enviar el mensaje. Intenta de nuevo más tarde.", "danger")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
