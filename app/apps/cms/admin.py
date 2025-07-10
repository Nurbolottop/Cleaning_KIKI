from django.contrib import admin
from apps.cms import models as cms_models
from django.utils.html import format_html

# Register your models here.

@admin.register(cms_models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'phone', 'work_schedule')
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'email', 'phone')
    
    fieldsets = (
        ('Основная информация', {
<<<<<<< HEAD
            'fields': ('title', 'description', 'logo','icon')
=======
            'fields': ('title', 'description', 'logo')
>>>>>>> 3da9a24fed32cd4ff816f1cc31908e8e39f2cc4a
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone', 'work_schedule','locate')
        }),
        ('Социальные сети', {
            'fields': ('whatsapp', 'telegram', 'instagram', 'facebook'),
            'classes': ('collapse',)
        }),
    )
<<<<<<< HEAD

@admin.register(cms_models.Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_2', 'preview_image', 'preview_icon')
    list_display_links = ('title',)
    search_fields = ('title', 'title_2', 'description')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_2', 'description')
        }),
        ('Изображения', {
            'fields': ('image', 'icon')
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;">', obj.image.url)
        return "Нет изображения"
    preview_image.short_description = 'Изображение'
    
    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-height: 50px;">', obj.icon.url)
        return "Нет иконки"
    preview_icon.short_description = 'Иконка'

    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }

    def has_add_permission(self, request):
        # Проверяем количество существующих слайдов
        if cms_models.Slide.objects.count() >= 3:
            return False
        return True
=======
    
    def has_add_permission(self, request):
        # Запрещаем создание новых объектов Settings если уже есть хотя бы один
        return not cms_models.Settings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление объекта Settings
        return False
>>>>>>> 3da9a24fed32cd4ff816f1cc31908e8e39f2cc4a
