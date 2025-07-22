from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    subject = models.CharField(max_length=150, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Создано")

    class Meta:
        verbose_name = "2) Сообщение"
        verbose_name_plural = "2) Сообщения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} – {self.phone}"


class Testimonial(models.Model):
    image = models.ImageField(upload_to='reviews/', verbose_name='Фото')
    name = models.CharField(max_length=50, verbose_name='Имя')
    service = models.ForeignKey(
        'extra.OurServices',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Услуга',
        related_name='testimonials'
    )
    description = models.TextField(verbose_name='Описание')
    show = models.BooleanField(default=False, verbose_name='Отображать')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '1) Отзыв'
        verbose_name_plural = '1) Отзывы'


class Booking(models.Model):
    """Модель заявки / брони на услугу."""
    service = models.ForeignKey(
        'extra.OurServices',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Услуга',
        related_name='bookings'
    ) 
    name = models.CharField(max_length=100, verbose_name='Имя заказчика')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    rooms = models.PositiveSmallIntegerField(verbose_name='Количество комнат')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Создано')
    more = models.TextField(verbose_name='Дополнительная информация', blank=True)

    def __str__(self):
        return f"{self.name} – {self.service} ({self.rooms} комн.)"

    class Meta:
        verbose_name = '3) Бронь / заказ'
        verbose_name_plural = '3) Брони / заказы'
        ordering = ['-created_at']

