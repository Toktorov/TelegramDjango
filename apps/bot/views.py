from django.shortcuts import render
from django.conf import settings
from telebot import TeleBot

bot = TeleBot("5607757460:AAEFDnw9IuEUx5ksYcSs2NdkUaeu9yGD4AQ", threaded=False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет")