from django.shortcuts import render
from django.conf import settings
from telebot import TeleBot, types
from apps.bot.models import User, UserPost
from apps.bot.keyboard import start_command
from telegram_bot_pagination import InlineKeyboardPaginator

bot = TeleBot(settings.TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(message:types.Message):
    User.objects.get_or_create(username = message.from_user.username, id_telegram=message.from_user.id, first_name = message.from_user.first_name, last_name = message.from_user.last_name, chat_id = message.chat.id)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, f"Привет {message.from_user.full_name}", reply_markup=start_command())

class Post():
    def __init__(self):
        self.title = None 
        self.description = None

post = Post()

def get_title(message:types.Message):
    post.title = message.text
    msg = bot.send_message(message.chat.id, "Отправьте описание")
    bot.register_next_step_handler(msg, get_description)

def get_description(message:types.Message):
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
        bot.send_message(message.chat.id, "Успешно создано", reply_markup=start_command())
    except TypeError:
        bot.send_message(message.chat.id, "Отправьте фотографию поста")
    except Exception as error:
        bot.send_message(message.chat.id, f"Произошла ошибка {error}")

@bot.message_handler(commands=['getpost']) 
def get_post(message:types.Message, page = 1):
    user = User.objects.get(id_telegram=message.from_user.id)
    users_post = UserPost.objects.all().filter(user_id = user.id)
    paginator = InlineKeyboardPaginator(
        len(users_post),
        current_page=page,
        data_pattern='character#{page}',
    )
    for post in users_post:
        bot.send_message(user.chat_id, f"ID поста: {post.id}\nНазвание: {post.title}\nОписание: {post.description}\nСоздан {post.created}")
        try:
            with open(f'media/{post.image}', 'rb') as image:
                bot.send_photo(user.chat_id, image)
        except:
            bot.send_message(user.chat_id, f"У поста ID: {post.id} нету фотографии")
    bot.send_message(
        user.chat_id,
        users_post[page-1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
        
@bot.message_handler(commands=['delete_post'])
def delete_post(message:types.Message):
    user = User.objects.get(id_telegram=message.from_user.id)
    msg = bot.send_message(user.chat_id, "Введите ID поста которую нужно удалить")
    bot.register_next_step_handler(msg, get_delete_post)

def get_delete_post(message:types.Message):
    bot.delete_message(message.chat.id, message.message_id)
    try:
        post_id = int(message.text)
        user = User.objects.get(id_telegram=message.from_user.id)
        post = UserPost.objects.get(id = post_id)
        if post.user.id == user.id:
            post.delete()
            bot.send_message(user.chat_id, f"Пост успешно удален")
        else:
            bot.send_message(user.chat_id, f"У вас нет прав на удаление поста")
    except UserPost.DoesNotExist:
        bot.send_message(user.chat_id, "ID поста которые вы ввели не найден")
    except ValueError:
        bot.send_message(user.chat_id, "Введите ID как целое число")

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    get_post(call, page)

@bot.callback_query_handler(func = lambda call: True)
def all_command(call):
    if call.data == 'create_post':
        msg = bot.send_message(call.message.chat.id, "Введите название поста: ")
        bot.register_next_step_handler(msg, get_title)
    elif call.data == "get_post":
        get_post(call)
    elif call.data == "delete_post":
        delete_post(call)

@bot.message_handler()  
def not_found(message:types.Message):
    bot.send_message(message.chat.id, "Я вас не понял")