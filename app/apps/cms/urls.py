
from django.urls import path
from apps.cms import views as cms_views
from apps.contacts import views as contacts_views
from apps.extra import views as extra_views

urlpatterns = [
    path('', cms_views.index, name='index'),
<<<<<<< HEAD
    path('about/', cms_views.about, name='about'),
    path('contacts/', cms_views.contacts, name='contacts'),
    path('services/', cms_views.services, name='services'),
    path('services/<int:id>/', cms_views.services_details, name='services_details'),
=======
>>>>>>> 3da9a24fed32cd4ff816f1cc31908e8e39f2cc4a
]