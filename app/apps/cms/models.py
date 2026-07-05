from django.db import models
from django_resized.forms import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField

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
        quality=85, 
        upload_to='slides/', 
        verbose_name="Изображение",
        null=True, blank=True
    )
    icon = ResizedImageField(
        force_format="WEBP", 
        quality=85, 
        upload_to='slides/', 
        verbose_name="Иконка",
        null=True, blank=True
    )
    class Meta:
        verbose_name = '3) Слайды'
        verbose_name_plural = '3) Слайды'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Мобильная версия фона (<name>_m.webp): телефоны получают ~3x меньший файл.
        # Используется через фильтр mobile_image_url в шаблоне слайдера.
        if self.image:
            try:
                import os
                from PIL import Image as PILImage
                path = self.image.path
                base, ext = os.path.splitext(path)
                img = PILImage.open(path)
                if img.width > 828:
                    img = img.resize((828, int(img.height * 828 / img.width)), PILImage.LANCZOS)
                img.save(base + '_m' + ext, 'WEBP', quality=70, method=6)
            except Exception:
                pass

    def __str__(self):
        return self.title

    
class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название статьи'
    )
    description = RichTextUploadingField(
        verbose_name='Описание статьи'
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='blog/', 
        verbose_name="Изображение",
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    class Meta:
        verbose_name = '2) Статьи'
        verbose_name_plural = '2) Статьи'
    def __str__(self):
        return self.title

class Projects(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название Организации'
    )
    duration = models.CharField(
        max_length=100,
        verbose_name='Длительность'
    )
    price = models.CharField(
        max_length=100,
        verbose_name='Стоимость'
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='process/', 
        verbose_name="Изображение",
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    service = models.ForeignKey(
        'extra.OurServices',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    class Meta:
        verbose_name = '4) Проекты'
        verbose_name_plural = '4) Проекты'
    def __str__(self):
        return self.title