from threading import Thread

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

from apps.extra.models import OurServices
from apps.telegram_bot.views import send_testimonial_message, send_booking_message
from .models import Testimonial, Booking


def process_booking(request):
    """Обрабатывает POST с формы бронирования (сайдбар / страница заказа).

    Использование в других view:
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

    # Уведомление в Telegram — в фоне, чтобы не блокировать ответ пользователю
    Thread(target=send_booking_message, args=(booking,), daemon=True).start()

    messages.success(request, "Суранычыңыз кабыл алынды!", extra_tags="booking_sent")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": True})

    return HttpResponseRedirect("/")


def testimonial_form(request):
    resp = process_booking(request)
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
            # Отправляем на модерацию в Telegram — в фоне
            Thread(target=send_testimonial_message, args=(testimonial,), daemon=True).start()
            messages.success(request, "Пикириңиз калтырылды, чоң рахмат!", extra_tags='reviewed')
            return redirect('index')
        else:
            messages.error(request, "Бардык талааларды туура толтуруңуз!")

    return render(request, 'forms/pages/testimonial_form.html')


def booking_form(request):
    resp = process_booking(request)
    if resp:
        return resp
    return render(request, 'forms/pages/booking_form.html')
