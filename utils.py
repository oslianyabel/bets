import logging

from telebot.types import ReplyKeyboardRemove

import markups as markups
from bot import bot
from database import db

logger = logging.getLogger("chatbot.utils")


def send_message(obj_msg, msg, markup=ReplyKeyboardRemove()):
    bot.send_chat_action(obj_msg.chat.id, "typing")
    bot.send_message(obj_msg.chat.id, msg, reply_markup=markup)


def edit_message(obj_msg, msg, markup=None):
    bot.send_chat_action(obj_msg.chat.id, "typing")
    if markup:
        bot.edit_message_text(
            msg, obj_msg.chat.id, obj_msg.message_id, reply_markup=markup
        )
    else:
        bot.edit_message_text(msg, obj_msg.chat.id, obj_msg.message_id)


def delete_message(obj_msg):
    bot.delete_message(obj_msg.chat.id, obj_msg.message_id)


def process_inline_button(buttom_name, obj_msg):
    logger.info(buttom_name)
    if buttom_name == "apuestas":
        markup = markups.apuestas_markup()
        msg = "Seleccione el deporte"
        edit_message(obj_msg, msg, markup)

    elif buttom_name == "apostar":
        markup = markups.apuestas_markup()
        msg = "Seleccione el deporte"
        send_message(obj_msg, msg, markup)

    elif buttom_name == "movimientos":
        markup = markups.movimientos_markup()
        msg = "Seleccione una opción"
        edit_message(obj_msg, msg, markup)

    elif buttom_name == "combinadas":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "bonos":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "terminos":
        msg = msg_terminos
        send_message(obj_msg, msg)

    elif buttom_name == "reglas":
        markup = markups.reglas_markup()
        msg = "Selecciona un deporte para ver sus reglas"
        edit_message(obj_msg, msg, markup)

    elif buttom_name == "futbol":
        markup = markups.futbol_markup()
        msg = "Seleccione la competición"
        edit_message(obj_msg, msg, markup)

    elif buttom_name == "beisbol":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "baloncesto":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "tenis":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "ufc":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "boxeo":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "futbol_americano":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "balonmano":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "mi_saldo":
        msg = "🛠️En desarrollo"
        #saldo = db.get_user()
        send_message(obj_msg, msg)

    elif buttom_name == "recarga":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "retiros":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "transferencia":
        msg = "🛠️En desarrollo"
        send_message(obj_msg, msg)

    elif buttom_name == "menu":
        markup = markups.menu_markup()
        msg = "Menú Principal"
        edit_message(obj_msg, msg, markup)

    else:
        logger.error(f"Botón {buttom_name} no registrado")
        msg = "Botón Inválido"
        send_message(obj_msg, msg)


msg_terminos = """‼️Por razones obvias, este bot de apuestas deportivas cuenta con sus propios reglamentos cuya lectura es importante antes de realizar cualquier apuesta⚠️

🔷 - En caso de un posible error de partidos o de cuotas nuestro equipo tendrá el derecho a reembolsar esas apuestas. También tendrá el derecho a detener el acceso a los botones durante la investigacion a usuarios que al retirar los # de teléfono o tarjeta no coincidan con los de depósito.

🔷 -  Ser mayor de edad👌

🔷 -  Los creadores dejan claro que usted siempre es responsable de cada apuesta y de que estés realizando la jugada deseada


🔷 - El jugador no puede anular una apuesta después de haberla formulado

🔷 - Si realiza un depósito a un número de cuenta equivocado o ponga mal el número para el retiro no nos hacemos responsables👌

🔷 - En caso de usted perder su cuenta de telegram o de retirarse del bot no existe recursos para recuperar su balance👌

🔷 - Podrá realizar su apuesta en cualquier horario del día siempre y cuando el partido al que apostará no haya comenzado👌

🔷 - Los horarios en los que se pagarán las apuestas son: 👇

⏰8:00 am hasta las 10:00 pm⏰

🔷 - Usted tiene el derecho a reclamar un posible error después que finalice un partido tres horas después y antes de las 24 horas de haberse finalizado👌

🔷 - Siempre debe de leer las acciones que está realizando en el bot, los botones y comandos que realiza son automáticos👌

🔷 - El usuario que sea expulsado o eliminado por incumplir cualquier regla, faltas de respeto a la administración o a cualquier usuario, por cometer fraude, haga spam sobre otras casas de apuestas o cualquier otro comportamiento indebido puede perder su fondo si la administración lo decide así... Aclaramos que esto solo pasará en situaciones extremas.👌

🔷 - Tus depósitos activos en el bot no deben superar los 20.000 CUP, si supera este límite debes retirar parte de tus fondos, no queremos comprometernos con este tipo de cosas, use un banco"""
