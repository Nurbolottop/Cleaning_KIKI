from django.contrib import admin
from django.utils.html import format_html

from .models import Testimonial, ContactMessage, Booking

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'service', 'short_description', 'show', 'image_tag')
    list_editable = ('show',)
    readonly_fields = ('image', 'name', 'service', 'description', 'image_tag')
    fields = ('image_tag', 'image', 'name', 'service', 'description', 'show')
    search_fields = ('name', 'service__title', 'description')
    list_filter = ('show', 'service')
    
    def short_description(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description
    short_description.short_description = 'Описание'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="object-fit:cover; border-radius:8px;"/>', obj.image.url)
        return '-'
    image_tag.short_description = 'Фото'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'phone', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'phone', 'subject', 'message', 'created_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    fields = ('service', 'name', 'phone', 'rooms', 'more', 'created_at')
    list_display = ('service', 'name', 'phone', 'rooms', 'more', 'created_at')
    search_fields = ('name', 'phone', 'service__title')
    list_filter = ('service', 'rooms', 'created_at')
    readonly_fields = ('service', 'name', 'phone', 'rooms', 'more', 'created_at')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        # Разрешаем любые изменения (только поле show доступно для редактирования через readonly_fields)
        return True
    def has_delete_permission(self, request, obj=None):
        return False
