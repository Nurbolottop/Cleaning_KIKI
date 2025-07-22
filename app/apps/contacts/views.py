from django.shortcuts import render, redirect
from apps.cms import models as cms_models
from apps.extra.models import OurServices
from .models import Testimonial
from apps.telegram_bot.views import send_testimonial_message
from .models import Booking
from django.http import HttpResponseRedirect
from django.contrib import messages

def process_booking(request, redirect_url=None):
    """Обрабатывает POST с бронированием.

    Использование в других view:
        if request.method == "POST":
            resp = process_booking(request)
            if resp:
                return resp
    """
    if request.method != "POST":
        return None

    service_id = request.POST.get("service")
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    rooms = request.POST.get("rooms")
    more = request.POST.get("more", "")

    # валидация
    if not (service_id and name and phone and rooms):
        return None

    try:
        rooms = int(rooms)
    except ValueError:
        return None

    service = OurServices.objects.filter(id=service_id).first()
    if not service:
        return None

    booking = Booking.objects.create(
        service=service,
        name=name,
        phone=phone,
        rooms=rooms,
        more=more,
    )

    # Отправить в Telegram (опционально)
    try:
        from apps.telegram_bot.views import send_booking_message  # type: ignore
        from threading import Thread
        Thread(target=send_booking_message, args=(booking,), daemon=True).start()
    except ImportError:
        pass

    messages.success(request, "Суранычыңыз кабыл алынды!", extra_tags="booking_sent")

    # AJAX request? Return JSON
    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        return JsonResponse({"success": True})

    return HttpResponseRedirect(request.path)

def testimonial_form(request):
    settings = cms_models.Settings.objects.first()
    services = OurServices.objects.all()

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = process_booking(request, redirect_url="index")
    if resp:
        return resp

    if request.method == 'POST':
        name = request.POST.get('name')
        service_id = request.POST.get('service')
        description = request.POST.get('description')
        image = request.FILES.get('photo')
        service = OurServices.objects.filter(id=service_id).first() if service_id else None

        if name and service and description and image:
            testimonial = Testimonial.objects.create(
                name=name,
                service=service,
                description=description,
                image=image,
            )
            # Send to Telegram for moderation
            send_testimonial_message(testimonial)
            messages.success(request, "Пикириңиз калтырылды, чоң рахмат!", extra_tags='reviewed')
            return redirect('index')
        else:
            messages.error(request, "Бардык талааларды туура толтуруңуз!")

    return render(request, 'forms/pages/testimonial_form.html', locals())

def booking_form(request):
    settings = cms_models.Settings.objects.first()
    services = OurServices.objects.all()

    # обработка формы бронирования, если она отправлена с главной страницы
    resp = process_booking(request, redirect_url="index")
    if resp:
        return resp
    return render(request, 'forms/pages/booking_form.html', locals())