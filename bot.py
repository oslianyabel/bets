import telebot
from config import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
