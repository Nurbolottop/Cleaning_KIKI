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
            'fields': ('title', 'description', 'logo','icon')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone', 'work_schedule','locate')
        }),
        ('Социальные сети', {
            'fields': ('whatsapp', 'telegram', 'instagram', 'facebook'),
            'classes': ('collapse',)
        }),
    )

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

# Blog Admin
@admin.register(cms_models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_preview', 'description_preview')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return 'No Image'
    image_preview.short_description = 'Превью изображения'
    
    def description_preview(self, obj):
        if obj.description:
            return format_html(obj.description[:150] + '...')
        return 'No Description'
    description_preview.short_description = 'Превью описания'

# Projects Admin
@admin.register(cms_models.Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'duration', 'price', 'created_at', 'image_preview')
    list_filter = ('service', 'created_at')
    search_fields = ('title', 'duration', 'price')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'service', 'duration', 'price')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Дополнительная информация', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return 'No Image'
    image_preview.short_description = 'Превью изображения'
