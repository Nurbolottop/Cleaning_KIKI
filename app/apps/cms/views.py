from django.shortcuts import render
from apps.cms import models as cms_models
# Create your views here.
def index(request):
    settings = cms_models.Settings.objects.first()
    return render(request, 'pages/base/index.html', locals())