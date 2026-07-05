from django.db import models
from django_resized.forms import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField

ICON_CHOICES = [
    ('icon-oosouji', 'Уборка'),
    ('icon-cleaning', 'Чистка'),
    ('icon-mop', 'Моп'),
    ('icon-vacuum', 'Пылесос'),
    ('icon-bucket', 'Ведро'),
    ('icon-sponge', 'Губка'),
    ('icon-broom', 'Метла'),
    ('icon-duster', 'Щетка'),
    ('icon-spray', 'Спрей'),
    ('icon-window', 'Окно'),
    ('icon-toilet', 'Туалет'),
    ('icon-kitchen', 'Кухня'),
    ('icon-bathroom', 'Ванная'),
    ('icon-carpet', 'Ковер'),
    ('icon-mattress', 'Матрас'),
    ('icon-furniture', 'Мебель'),
    ('icon-air', 'Воздух'),
    ('icon-laundry', 'Прачечная'),
    ('icon-disinfection', 'Дезинфекция'),
    ('icon-eco', 'Экологичность'),
    ('icon-quality', 'Качество'),
]

class About(models.Model):
    # Раньше save() принудительно ужимал фото до 280x250 — на retina-экранах
    # они выходили мыльными. Теперь размером/форматом занимается ResizedImageField.

    image_1 = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='about/', 
        verbose_name="Изображение 1",
        null=True, blank=True
    )
    image_2 = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='about/', 
        verbose_name="Изображение 2",
        null=True, blank=True
    )
    image_3 = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='about/', 
        verbose_name="Изображение 3",
        null=True, blank=True
    )
    image_4 = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='about/', 
        verbose_name="Изображение 4",
        null=True, blank=True
    )
    title_1 = models.CharField(
        max_length=100,
        verbose_name='Название 1'
    )
    title_2 = models.CharField(
        max_length=100,
        verbose_name='Название c синим текстом'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    experience = models.CharField(
        max_length=100,
        verbose_name='Опыт'
    )
    customers = models.CharField(
        max_length=100,
        verbose_name='Дофольны Клиенты( в процентах )'
    )
    successfully = models.CharField(
        max_length=100,
        verbose_name='Успешно выполнено( в цифрах )'
    )
    time  = models.CharField(
        max_length=100,
        verbose_name='Время работы'
    )
    number = models.CharField(
        max_length=100,
        verbose_name='Номер для связи'
    )
    class Meta:
        verbose_name = '1) О нас'
        verbose_name_plural = '1) О нас'
    def __str__(self):
        return self.title_1

class Mission(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='missions')
    title = models.CharField(
        max_length=100,
        verbose_name='Название миссии'
    )

    class Meta:
        verbose_name = 'Миссия'
        verbose_name_plural = 'Миссии'
    def __str__(self):
        return self.title

class OurServices(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название Услуги'
    )
    subtitle = models.CharField(
        verbose_name='Подзаголовок Услуги',
        max_length=100,
    )
    category = models.CharField(
        verbose_name='Категория Услуги',
        max_length=100,
    )
    description = RichTextUploadingField(
        verbose_name='Описание Услуги'
    )
    price = models.CharField(
        max_length=50,
        verbose_name='Цена',
        help_text='Например: 5000'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    ICON_CHOICES = [
        ('icon-oosouji', 'Уборка'),
        ('icon-cleaning', 'Чистка'),
        ('icon-mop', 'Моп'),
        ('icon-vacuum', 'Пылесос'),
        ('icon-bucket', 'Ведро'),   
        ('icon-sponge', 'Губка'),
        ('icon-broom', 'Метла'),
        ('icon-duster', 'Щетка'),
        ('icon-spray', 'Спрей'),
        ('icon-window', 'Окно'),
        ('icon-toilet', 'Туалет'),
        ('icon-kitchen', 'Кухня'),
        ('icon-bathroom', 'Ванная'),
        ('icon-carpet', 'Ковер'),
        ('icon-mattress', 'Матрас'),
        ('icon-furniture', 'Мебель'),
        ('icon-air', 'Воздух'),
        ('icon-laundry', 'Прачечная'),
        ('icon-disinfection', 'Дезинфекция'),
        ('icon-eco', 'Экологичность'),
        ('icon-quality', 'Качество'),
    ]
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        verbose_name='Иконка Услуги'
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='services/', 
        verbose_name="Изображение Услуги",
        null=True, blank=True
    )
    banner_image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='services/', 
        verbose_name="Баннер Услуги",
        null=True, blank=True
    )
    class Meta:
        verbose_name = '2) Услуги'
        verbose_name_plural = '2) Услуги'
        ordering = ['order']
    def __str__(self):
        return self.title
    
class ServicePoint(models.Model):
    service = models.ForeignKey('OurServices', on_delete=models.CASCADE, related_name='points')
    title = models.CharField(
        max_length=100,
        verbose_name='Название пункта'
    )
    class Meta:
        verbose_name = 'Пункт услуги'
        verbose_name_plural = 'Пункты услуги'
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Proccess(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название Процесса'
    )
    description = models.TextField(
        verbose_name='Описание Процесса'
    )
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        verbose_name='Иконка Услуги'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    class Meta:
        verbose_name = '3) Процесс'
        verbose_name_plural = '3) Процессы'
        ordering = ['order']
    def __str__(self):
        return self.title   


class Metric(models.Model):
    projects_per_month = models.IntegerField(
        default=0, 
        verbose_name='Проекты в месяц'
    )  
    happy_customers = models.IntegerField(
        default=0, 
        verbose_name='Довольные клиенты'
    )       
    positive_reviews = models.IntegerField(
        default=0, 
        verbose_name='Положительные отзывы'
    )      
    cleaned_area_m2 = models.IntegerField(
        default=0, 
        verbose_name='Чистая площадь'
    )    

    class Meta:
        verbose_name = '4) Мы в числах'
        verbose_name_plural = '4) Мы в числах'
    def __str__(self):
        return f"{self.projects_per_month} — {self.happy_customers}"

class Team(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность'
    )
    experience = models.IntegerField(
        verbose_name='Опыт'
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='team/', 
        verbose_name="Изображение",
        null=True, blank=True
    )   
    status = models.BooleanField(
        default=False,
        verbose_name='Статус'
    )
    class Meta:
        verbose_name = '5) Команда'
        verbose_name_plural = '5) Команда'
    def __str__(self):
        return self.name

class BeforeAfter(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    before_image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='before_after/', 
        verbose_name="Изображение до",
        null=True, blank=True
    )
    after_image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='before_after/', 
        verbose_name="Изображение после",
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    
    class Meta:
        verbose_name = '5) До и После'
        verbose_name_plural = '5) До и После'
        ordering = ['order']
    
    def __str__(self):
        return self.title
