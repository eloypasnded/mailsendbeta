import telebot
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Token del bot de Telegram
TOKEN = '7128002872:AAGxG9H0dXjdI7h6vf-CjApsR319JpMa0Zg'
bot = telebot.TeleBot(TOKEN)

# Información del servidor SMTP y credenciales de correo electrónico
smtp_server = 'smtp.yandex.com'
smtp_port = 465
email_user = 'ernp05@yandex.ru'
email_password = 'LoliconMaster'
email_send_to = 'ernp@nauta.cu'

# Manejador para mensajes que contienen multimedia
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio'])
def handle_docs_audio(message):
    # Obtiene el archivo multimedia del mensaje
    file_info = bot.get_file(message.document.file_id)
    
    # Descarga el archivo
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = 'archivo_descargado'
    
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Configura el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send_to
    msg['Subject'] = 'Archivo enviado desde el bot de Telegram'

    # Adjunta el archivo al mensaje
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(file_name, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
    msg.attach(part)
    
    # Conecta al servidor SMTP y envía el correo
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(email_user, email_password)
    server.send_message(msg)
    server.quit()
    
    # Responde al mensaje con "Hecho"
    bot.reply_to(message, 'Hecho')

# Inicia el bot
bot.polling()
