from django.shortcuts import render
from django.conf import settings
from telebot import TeleBot
from apps.bot.models import User, UserPost

bot = TeleBot(settings.TOKEN, threaded=False)

class Post:
    def __init__(self):
        self.title = None 
        self.description = None

post = Post()

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = User.objects.get(id_telegram=message.from_user.id)
    except:
        User.objects.create(username = message.from_user.username, id_telegram=message.from_user.id, first_name = message.from_user.first_name, last_name = message.from_user.last_name, chat_id = message.chat.id)
    bot.send_message(message.chat.id, f"Привет {message.from_user.id}")

@bot.message_handler(commands=['create_post'])
def create_post(message):
    msg = bot.send_message(message.chat.id, "Создать пользователя")
    bot.send_message(message.chat.id, "Введите название поста: ")
    bot.register_next_step_handler(msg, get_title)

def get_title(message):
    post.title = message.text
    msg = bot.send_message(chat_id=message.chat.id, text = "Отправьте описание")
    bot.register_next_step_handler(msg, get_description)

def get_description(message):
    post.description = message.text
    msg = bot.send_message(chat_id=message.chat.id, text = "Данные сохранены")
    try:
        user = User.objects.get(id_telegram=message.from_user.id)
        UserPost.objects.create(user_id = user.id, title = post.title, description = post.description)
        bot.send_message(chat_id=message.chat.id, text="Успешно создано")
    except:
        bot.send_message(chat_id=message.chat.id, text = "Произошла ошибка")

@bot.message_handler(commands=['getpost'])
def get_post(message):
    user = User.objects.get(id_telegram=message.from_user.id)
    for post in UserPost.objects.all().filter(user_id = user.id):
        bot.send_message(chat_id=message.chat.id, text = f"ID поста: {post.id}\nНазвание: {post.title}\nОписание: {post.description}")
        
# @bot.message_handler(commands=['delete_post'])
# def delete_post(message):
#     user = User.objects.get(id_telegram=message.from_user.id)

    
@bot.message_handler()
def not_found(message):
    bot.send_message(chat_id = message.chat.id, text = "Я вас не понял")