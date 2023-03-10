from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized.forms import ResizedImageField

# Create your models here.
class User(AbstractUser):
    id_telegram = models.PositiveBigIntegerField(
        verbose_name="ID телеграмм пользователя",
        null = True
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия",
        blank=True, null = True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name="Имя",
        blank=True, null = True
    )
    chat_id = models.PositiveBigIntegerField(
        verbose_name="CHAT ID",
        null = True
    )

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class UserPost(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="users_post",
        verbose_name="Пост пользователя"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='post_images/',
        verbose_name="Фотография проекта",
        blank = True, null = True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.title}"

    class Meta:
        verbose_name = "Пост пользователя"
        verbose_name_plural = "Посты пользователей"