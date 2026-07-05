import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.cms import models as cms_models
from apps.extra import models as extra_models
from apps.contacts import models as contacts_models
from apps.contacts import views as contacts_views

# `settings` (настройки сайта) и `services` (список услуг) доступны на каждой
# странице через context processor apps.cms.context_processors.site_settings —
# в самих view их запрашивать не нужно.


def index(request):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp

    slides = cms_models.Slide.objects.all()
    about = extra_models.About.objects.prefetch_related('missions').first()
    process = extra_models.Proccess.objects.all()
    before_after = extra_models.BeforeAfter.objects.all()[:2]
    testimonials = contacts_models.Testimonial.objects.filter(show=True).select_related('service')
    projects = cms_models.Projects.objects.select_related('service').all()[:9]

    # Команда: берём по 3 случайных из чётных и нечётных позиций
    all_members = list(extra_models.Team.objects.filter(status=True))
    even_members = all_members[1::2]
    odd_members = all_members[::2]
    random.shuffle(even_members)
    random.shuffle(odd_members)
    team_members = even_members[:3] + odd_members[:3]

    return render(request, 'pages/base/index.html', {
        'slides': slides,
        'about': about,
        'process': process,
        'before_after': before_after,
        'testimonials': testimonials,
        'projects': projects,
        'team_members': team_members,
    })


def about(request):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp

    return render(request, 'pages/base/about.html', {
        'about': extra_models.About.objects.prefetch_related('missions').first(),
        'process': extra_models.Proccess.objects.all(),
        'metric': extra_models.Metric.objects.first(),
        'team': extra_models.Team.objects.all(),
        'testimonials': contacts_models.Testimonial.objects.filter(show=True).select_related('service'),
    })


def contacts(request):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")

        if name and phone and subject and message_text:
            contact_obj = contacts_models.ContactMessage.objects.create(
                name=name,
                phone=phone,
                subject=subject,
                message=message_text,
            )
            from threading import Thread
            from apps.telegram_bot.views import send_contact_message
            Thread(target=send_contact_message, args=(contact_obj,), daemon=True).start()
            messages.success(request, "Сиздин билдирүү жөнөтүлдү!", extra_tags="contact_sent")
            return redirect("index")
        else:
            messages.error(request, "Бардык талааларды туура толтуруңуз!")

    return render(request, 'pages/base/contact.html', {
        'metric': extra_models.Metric.objects.first(),
    })


def services(request):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp
    return render(request, 'pages/base/services.html')


def services_details(request, id):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp
    service = get_object_or_404(
        extra_models.OurServices.objects.prefetch_related('points'), id=id
    )
    return render(request, 'pages/details/service_detail.html', {'service': service})


def team(request):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp
    return render(request, 'pages/base/team.html', {
        'team': extra_models.Team.objects.all(),
    })


def blog(request):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp
    return render(request, 'pages/base/blog.html', {
        'blogs': cms_models.Blog.objects.all(),
    })


def blog_details(request, id):
    resp = contacts_views.process_booking(request)
    if resp:
        return resp
    blog = get_object_or_404(cms_models.Blog, id=id)
    return render(request, 'pages/details/blog-details.html', {'blog': blog})
