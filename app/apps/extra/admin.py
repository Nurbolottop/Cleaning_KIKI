from django.contrib import admin
from django.utils.html import format_html
from apps.extra import models as extra_models

class MissionInline(admin.StackedInline):
    model = extra_models.Mission
    extra = 1

class AboutAdmin(admin.ModelAdmin):
    list_display = ('title_1', 'preview_image_1', 'preview_image_2', 'preview_image_3', 'preview_image_4')
    list_display_links = ('title_1',)
    inlines = [MissionInline]
    
    def preview_image_1(self, obj):
        if obj.image_1:
            return format_html('<img src="{}" width="100" height="89" />', obj.image_1.url)
        return '-'
    preview_image_1.short_description = 'Image 1 Preview'
    
    def preview_image_2(self, obj):
        return format_html('<img src="{}" width="100" height="104" />', obj.image_2.url if obj.image_2 else '#')
    preview_image_2.short_description = 'Image 2 Preview'
    
    def preview_image_3(self, obj):
        return format_html('<img src="{}" width="100" height="104" />', obj.image_3.url if obj.image_3 else '#')
    preview_image_3.short_description = 'Image 3 Preview'
    
    def preview_image_4(self, obj):
        return format_html('<img src="{}" width="100" height="104" />', obj.image_4.url if obj.image_4 else '#')
    preview_image_4.short_description = 'Image 4 Preview'
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title_1',
                'title_2',
                'description',
            )
        }),
        ('Изображения', {
            'fields': (
                'image_1',
                'image_2',
                'image_3',
                'image_4',
            )
        }),
        ('Статистика', {
            'fields': (
                'experience',
                'customers',
                'successfully',
            )
        }),
        ('Время работы', {
            'fields': (
                'time',
                'number',
            )
        }),
    )

admin.site.register(extra_models.About, AboutAdmin)

class ServicePointInline(admin.StackedInline):
    model = extra_models.ServicePoint
    extra = 1

@admin.register(extra_models.OurServices)
class OurServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'preview_image', 'icon', 'order')
    list_display_links = ('title',)
    inlines = [ServicePointInline]
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    preview_image.short_description = 'Изображение'

@admin.register(extra_models.Proccess)
class ProccessAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_icon', 'order')
    list_display_links = ('title',)
    
    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<span class="{}"></span>', obj.icon)
        return '-'
    preview_icon.short_description = 'Icon Preview'
    
    def has_add_permission(self, request):
        return False
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['icon'].choices = [(k, v) for k, v in form.base_fields['icon'].choices if k != '']
        return form

@admin.register(extra_models.SeriviceList)
class SeriviceListAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)

@admin.register(extra_models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'preview_image')
    list_display_links = ('name',)
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    preview_image.short_description = 'Изображение'

@admin.register(extra_models.BeforeAfter)
class BeforeAfterAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_before_image', 'preview_after_image', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)
    
    def preview_before_image(self, obj):
        if obj.before_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.before_image.url)
        return '-'
    preview_before_image.short_description = 'Изображение до'
    
    def preview_after_image(self, obj):
        if obj.after_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.after_image.url)
        return '-'
    preview_after_image.short_description = 'Изображение после'
    list_display = ('title', 'preview_before', 'preview_after', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)
    
    def preview_before(self, obj):
        if obj.before_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.before_image.url)
        return '-'
    preview_before.short_description = 'Фото до'
    
    def preview_after(self, obj):
        if obj.after_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.after_image.url)
        return '-'
    preview_after.short_description = 'Фото после'

@admin.register(extra_models.Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('projects_per_month', 'happy_customers', 'positive_reviews', 'cleaned_area_m2')
    list_display_links = ('projects_per_month',)
    list_editable = ('happy_customers', 'positive_reviews', 'cleaned_area_m2')
