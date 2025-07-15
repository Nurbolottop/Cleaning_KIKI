from django.shortcuts import render, redirect
from apps.cms import models as cms_models
from apps.extra.models import OurServices
from .models import Testimonial
from django.contrib import messages

def testimonial_form(request):
    settings = cms_models.Settings.objects.first()
    services = OurServices.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        service_id = request.POST.get('service')
        description = request.POST.get('description')
        image = request.FILES.get('photo')
        service = OurServices.objects.filter(id=service_id).first() if service_id else None

        if name and service and description and image:
            Testimonial.objects.create(
                name=name,
                service=service,
                description=description,
                image=image,
            )
            messages.success(request, "Пикириңиз калтырылды, чоң рахмат!", extra_tags='reviewed')
            return redirect('index')
        else:
            messages.error(request, "Бардык талааларды туура толтуруңуз!")

    return render(request, 'forms/pages/testimonial_form.html', locals())