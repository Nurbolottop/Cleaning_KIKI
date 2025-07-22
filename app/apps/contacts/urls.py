
from django.urls import path
from apps.cms import views as cms_views
from apps.contacts import views as contacts_views
from apps.extra import views as extra_views

urlpatterns = [
    path('testimonial-form/', contacts_views.testimonial_form, name='testimonial_form'),
    path('booking-form/', contacts_views.booking_form, name='booking_form'),
]