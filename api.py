# Dev: OslianyAbel
import logging
import os
import time

from flask import Flask, make_response, request
from telebot.types import Update

from bot import bot
from config import config
from database import db
from logging_conf import configure_logging
from markups import menu_markup
from utils import process_inline_button, send_message

configure_logging()
logger = logging.getLogger("chatbot.api")

app = Flask(__name__)

db.connect()

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=config.URL_BOT)
logger.info(f"webhook set in {config.URL_BOT}")

save_path = "images/"
if not os.path.exists(save_path):
    os.makedirs(save_path)

users = {}  # states control flow
welcome_msg = """Bienvenid@ a 🎲APUESTAS ⚽️DEPORTIVAS 🇨🇺CUBA. Aquí puedes realizar apuestas deportivas de forma fácil y segura.
Elige una opción para empezar:"""


@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_body = request.get_data()
        update = Update.de_json(json_body.decode("utf-8"))
        bot.process_new_updates([update])
        return make_response("OK", 200)

    return make_response("Invalid content-type", 400)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    logger.info("/start")
    user = db.get_user(message.from_user.id)
    if not user:
        data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        }
        db.create_user(data)

    msg = f"¡Hola {message.from_user.first_name}! 👋" + welcome_msg
    send_message(message, msg, menu_markup())


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    process_inline_button(call.data, call.message)


@bot.message_handler(commands=["saldo"])
def cmd_saldo(message):
    logger.info("/saldo")
    user = db.get_user(message.from_user.id)
    send_message(message, f"Su balance actual es de {user['balance']}CUP")


@bot.message_handler(commands=["apostar"])
def cmd_apostar(message):
    logger.info("/apostar")
    process_inline_button("apostar", message)


@bot.message_handler(commands=["apuestasactivas"])
def cmd_apuestasactivas(message):
    logger.info("/apuestasactivas")
    bets = db.get_user_bets(message.from_user.id, "pending")
    send_message(message, f"Sus apuestas activas son: {bets}")


@bot.message_handler(commands=["apuestaspasadas"])
def cmd_apuestaspasadas(message):
    logger.info("/apuestaspasadas")
    bets_win = db.get_user_bets(message.from_user.id, "win")
    bets_lose = db.get_user_bets(message.from_user.id, "lose")
    send_message(
        message, f"Apuestas ganadas: {bets_win}\nApuestas perdidas: {bets_lose}"
    )


@bot.message_handler(commands=["recargar"])
def cmd_recargar(message):
    logger.info("/recargar")
    send_message(
        message, "Hola, bienvenido al mejor bot de apuestas deportivas de Cuba!"
    )


@bot.message_handler(commands=["top"])
def cmd_top(message):
    logger.info("/top")
    send_message(
        message, "Hola, bienvenido al mejor bot de apuestas deportivas de Cuba!"
    )


@bot.message_handler(commands=["misreferidos"])
def cmd_misreferidos(message):
    logger.info("/misreferidos")
    send_message(
        message, "Hola, bienvenido al mejor bot de apuestas deportivas de Cuba!"
    )


@bot.message_handler(content_types=["text"])
def reply_text(message):
    logger.info(f"- User: {message.text}")
    send_message(message, "AI response...")


@bot.message_handler(content_types=["photo"])
def handle_photos(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_name = f"{file_id}.jpg"
        with open(os.path.join(save_path, file_name), "wb") as new_file:
            new_file.write(downloaded_file)

        logger.info("Imagen descargada")
        bot.reply_to(message, "¡Imagen recibida y guardada! Gracias")

    except Exception as exc:
        logger.error(exc)
        bot.reply_to(message, "Ocurrió un error al procesar tu imagen")
