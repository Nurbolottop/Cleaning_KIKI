from django.db import models
from django_resized.forms import ResizedImageField

# Create your models here.
class Settings(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название сайта'
    )
    description = models.TextField(
        verbose_name='Описание сайта'
    )
    logo = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='logo/', 
        verbose_name="Логотип",
        null=True, blank=True
    )
    icon = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='icon/', 
        verbose_name="Иконка",
        null=True, blank=True
    )
    locate = models.CharField(
        max_length=100,
        verbose_name='Адрес'
    )
    email = models.EmailField(
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=100,
        verbose_name='Телефон'
    )
    work_schedule = models.CharField(
        max_length=100,
        verbose_name='Режим работы'
    )
    whatsapp = models.URLField(
        verbose_name='Whatsapp'
    )
    telegram = models.URLField(
        verbose_name='Telegram'
    )
    instagram = models.URLField(
        verbose_name='Instagram'
    )  
    facebook = models.URLField(
        verbose_name='Facebook'
    )
    class Meta:
        verbose_name = '1) Настройки'
        verbose_name_plural = '1) Настройки'
    def __str__(self):
        return self.title

class Slide(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название слайда'
    )
    title_2 = models.CharField(
        max_length=100,
        verbose_name='Название слайда под желтым'
    )
    description = models.TextField(
        verbose_name='Описание слайда'
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='slides/', 
        verbose_name="Изображение",
        null=True, blank=True
    )
    icon = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='slides/', 
        verbose_name="Иконка",
        null=True, blank=True
    )
    class Meta:
        verbose_name = '2) Слайды'
        verbose_name_plural = '2) Слайды'

    def __str__(self):
        return self.title

    
