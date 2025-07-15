from django.db import models

# Create your models here.

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
