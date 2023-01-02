from django.core.management.base import BaseCommand
from apps.bot.views import bot

class Command(BaseCommand):
    help = 'Bot' 

    def handle(self, *args, **kwargs):
        print("START TELEGRAM BOT")
        print("https://t.me/django_tele_cryxxen_bot")
        bot.polling(none_stop=True, interval=0)