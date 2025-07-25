from django.shortcuts import render, redirect
from django.contrib import messages
from apps.cms import models as cms_models
from apps.extra import models as extra_models
from apps.contacts import models as contacts_models
from apps.contacts import views as contacts_views
# Create your views here.

def index(request):
    settings = cms_models.Settings.objects.first()
    slides = cms_models.Slide.objects.all()
    about = extra_models.About.objects.first()
    services = extra_models.OurServices.objects.all()
    process = extra_models.Proccess.objects.all()
    before_after = extra_models.BeforeAfter.objects.all()[:2]
    testimonials = contacts_models.Testimonial.objects.all()
    projects = cms_models.Projects.objects.all()[:9]  # Показываем первые 9 проектов (3 ряда по 3)
    
    # Get all active team members
    all_members = list(extra_models.Team.objects.filter(status=True))
    
    # Split into even and odd
    even_members = [m for i, m in enumerate(all_members) if (i + 1) % 2 == 0]
    odd_members = [m for i, m in enumerate(all_members) if (i + 1) % 2 != 0]
    
    # Randomly select 3 from each group
    import random
    random.shuffle(even_members)
    random.shuffle(odd_members)
    
    # Take first 3 from each
    team_members = even_members[:3] + odd_members[:3]

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    
    return render(request, 'pages/base/index.html', locals())

def about(request):
    settings = cms_models.Settings.objects.first()
    about = extra_models.About.objects.first()
    services = extra_models.OurServices.objects.all()
    process = extra_models.Proccess.objects.all()
    metric = extra_models.Metric.objects.first()
    team = extra_models.Team.objects.all()
    testimonials = contacts_models.Testimonial.objects.all()

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    
    return render(request, 'pages/base/about.html', locals())



def contacts(request):
    settings = cms_models.Settings.objects.first()
    metric = extra_models.Metric.objects.first()

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
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
            # Отправить в Telegram
            from threading import Thread
            from apps.telegram_bot.views import send_contact_message
            Thread(target=send_contact_message, args=(contact_obj,), daemon=True).start()
            messages.success(request, "Сиздин билдирүү жөнөтүлдү!", extra_tags="contact_sent")
            return redirect("index")
        else:
            messages.error(request, "Бардык талааларды туура толтуруңуз!")

    return render(request, 'pages/base/contact.html', locals())

def services(request):
    settings = cms_models.Settings.objects.first()
    services = extra_models.OurServices.objects.all()
    
    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    return render(request, 'pages/base/services.html', locals())

def services_details(request,id):
    settings = cms_models.Settings.objects.first()
    services = extra_models.OurServices.objects.get(id=id)

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    return render(request, 'pages/details/service_detail.html', locals())

def team(request):
    settings = cms_models.Settings.objects.first()
    team = extra_models.Team.objects.all()

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    return render(request, 'pages/base/team.html', locals())

def blog(request):
    settings = cms_models.Settings.objects.first()
    blogs = cms_models.Blog.objects.all()

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    return render(request, 'pages/base/blog.html', locals())

def blog_details(request,id):
    settings = cms_models.Settings.objects.first()
    blog = cms_models.Blog.objects.get(id=id)

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = contacts_views.process_booking(request, redirect_url="index")
    if resp:
        return resp
    return render(request, 'pages/details/blog-details.html', locals())