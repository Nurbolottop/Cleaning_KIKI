from django.urls import path
from apps.cms import views as cms_views
from apps.cms import seo

urlpatterns = [
    path('', cms_views.index, name='index'),
    path('about/', cms_views.about, name='about'),
    path('contacts/', cms_views.contacts, name='contacts'),
    path('services/', cms_views.services, name='services'),
    path('services/<int:id>/', cms_views.services_details, name='services_details'),
    path('team/', cms_views.team, name='team'),
    path('blog/', cms_views.blog, name='blog'),
    path('blog/<int:id>/', cms_views.blog_details, name='blog_details'),
    path('sitemap.xml', seo.sitemap_xml, name='sitemap'),
    path('robots.txt', seo.robots_txt, name='robots'),
]
