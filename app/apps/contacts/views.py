from django.shortcuts import render
from apps.cms import models as cms_models
from apps.extra import models as extra_models

# Create your views here.

def testimonial_form(request):
    settings = cms_models.Settings.objects.first()
    return render(request, 'forms/pages/testimonial_form.html', locals())