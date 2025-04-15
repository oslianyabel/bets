# database sync, without FastAPI, telebot
import logging

from bot import bot
from database import db
from logging_conf import configure_logging
from markups import menu_markup
from utils import process_inline_button, send_message

configure_logging()
logger = logging.getLogger("chatbot.polling")
welcome_msg = """Bienvenid@ a 🎲APUESTAS ⚽️DEPORTIVAS 🇨🇺CUBA. Aquí puedes realizar apuestas deportivas de forma fácil y segura.
Elige una opción para empezar:"""


@bot.message_handler(commands=["start"])
def cmd_start(message):
    logger.info("/start")
    user = db.get_user(message.from_user.id)
    logger.debug(user)
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
    send_message(
        message, "Hola, bienvenido al mejor bot de apuestas deportivas de Cuba!"
    )


@bot.message_handler(commands=["apuestas"])
def cmd_apuestas(message):
    logger.info("/apuestas")
    send_message(
        message, "Hola, bienvenido al mejor bot de apuestas deportivas de Cuba!"
    )


@bot.message_handler(commands=["misapuestas"])
def cmd_misapuestas(message):
    logger.info("/misapuestas")
    send_message(
        message, "Hola, bienvenido al mejor bot de apuestas deportivas de Cuba!"
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


if __name__ == "__main__":
    db.connect()
    bot.remove_webhook()
    logger.info("Polling started...")
    bot.polling()
    db.disconnect()
