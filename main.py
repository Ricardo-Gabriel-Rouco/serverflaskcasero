from flask import Flask, render_template_string, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters
import threading

# Configura tu token y crea el bot
TELEGRAM_TOKEN = 'TU_TOKEN_AQUI'
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# ----- Handlers de Telegram -----
def start(update, context):
    update.message.reply_text('¡Hola! Soy un bot en Raspberry Pi.')

def echo(update, context):
    update.message.reply_text(update.message.text)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(filters.TEXT, echo))

# ----- Flask app -----
app = Flask(__name__)

# Interfaz simple accesible por red local
@app.route("/")
def home():
    return render_template_string('''
        <h1>Servidor Flask en Raspberry Pi</h1>
        <form action="/enviar_telegram" method="post">
            <input name="mensaje" placeholder="Mensaje a Telegram">
            <button type="submit">Enviar a Telegram</button>
        </form>
    ''')

@app.route("/enviar_telegram", methods=["POST"])
def enviar_telegram():
    mensaje = request.form.get("mensaje")
    # Cambia el chat_id por el correcto de tu bot o usuario
    bot.send_message(chat_id="TU_CHAT_ID_AQUI", text=mensaje)
    return "Mensaje enviado a Telegram."

# ----- Launch Flask y Dispatcher -----
def telegram_polling():
    from telegram.ext import Updater
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher = dispatcher
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # Arrancar el bot de Telegram en un thread
    threading.Thread(target=telegram_polling, daemon=True).start()
    # El servidor Flask escuchará en todas las interfaces de red local
    app.run(host="0.0.0.0", port=5000)
