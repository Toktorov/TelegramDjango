from django.shortcuts import render
from django.conf import settings
from telebot import TeleBot
from apps.bot.models import User, UserPost

bot = TeleBot(settings.TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = User.objects.get(id_telegram=message.from_user.id)
    except:
        User.objects.create(username = message.from_user.username, id_telegram=message.from_user.id, first_name = message.from_user.first_name, last_name = message.from_user.last_name, chat_id = message.chat.id)
    bot.send_message(message.chat.id, f"Привет {message.from_user.full_name}")

class Post():
    def __init__(self):
        self.title = None 
        self.description = None
        self.image = None

post = Post()

@bot.message_handler(commands=['create_post'])
def create_post(message):
    msg = bot.send_message(message.chat.id, "Введите название поста: ")
    bot.register_next_step_handler(msg, get_title)

def get_title(message):
    post.title = message.text
    msg = bot.send_message(message.chat.id, "Отправьте описание")
    bot.register_next_step_handler(msg, get_description)

def get_description(message):
    post.description = message.text
    msg = bot.send_message(message.chat.id, "Отправьте фотографию поста")
    bot.register_next_step_handler(msg, get_image)
    
def get_image(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"media/post_images/{file_id}.webp", 'wb') as new_file:
            new_file.write(downloaded_file)
        user = User.objects.get(id_telegram=message.from_user.id)
        UserPost.objects.create(user_id = user.id, title = post.title, description = post.description, image = f"post_images/{file_id}.webp")
        bot.send_message(message.chat.id, "Успешно создано")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")

@bot.message_handler(commands=['getpost'])
def get_post(message):
    user = User.objects.get(id_telegram=message.from_user.id)
    for post in UserPost.objects.all().filter(user_id = user.id):
        bot.send_message(message.chat.id, f"ID поста: {post.id}\nНазвание: {post.title}\nОписание: {post.description}\nФотография: {post.image}\nСоздан {post.created}")
        
@bot.message_handler(commands=['delete_post'])
def delete_post(message):
    msg = bot.send_message(message.chat.id, "Введите ID поста которую нужно удалить")
    bot.register_next_step_handler(msg, get_delete_post)

def get_delete_post(message):
    try:
        post_id = int(message.text)
        user = User.objects.get(id_telegram=message.from_user.id)
        post = UserPost.objects.get(id = post_id)
        if post.user.id == user.id:
            post.delete()
            bot.send_message(message.chat.id, f"Пост успешно удален")
        else:
            bot.send_message(message.chat.id, f"У вас нет прав на удаление поста")
    except UserPost.DoesNotExist:
        bot.send_message(message.chat.id, "ID поста которые вы ввели не найден")
    except ValueError:
        bot.send_message(message.chat.id, "Введите ID как целое число")

@bot.message_handler()
def not_found(message):
    bot.send_message(message.chat.id, "Я вас не понял")