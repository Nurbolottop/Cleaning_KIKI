from django.shortcuts import render
from apps.cms import models as cms_models
from apps.extra import models as extra_models
# Create your views here.

def index(request):
    settings = cms_models.Settings.objects.first()
    slides = cms_models.Slide.objects.all()
    about = extra_models.About.objects.first()
    services = extra_models.OurServices.objects.all()
    process = extra_models.Proccess.objects.all()
    service_list = extra_models.SeriviceList.objects.all()
    before_after = extra_models.BeforeAfter.objects.all()[:2]
    
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
    
    return render(request, 'pages/base/index.html', locals())

def about(request):
    settings = cms_models.Settings.objects.first()
    about = extra_models.About.objects.first()
    services = extra_models.OurServices.objects.all()
    process = extra_models.Proccess.objects.all()
    service_list = extra_models.SeriviceList.objects.all()
    metric = extra_models.Metric.objects.first()
    team = extra_models.Team.objects.all()
    return render(request, 'pages/base/about.html', locals())

def contacts(request):
    settings = cms_models.Settings.objects.first()
    metric = extra_models.Metric.objects.first()
    return render(request, 'pages/base/contact.html', locals())

def services(request):
    settings = cms_models.Settings.objects.first()
    services = extra_models.OurServices.objects.all()
    return render(request, 'pages/base/services.html', locals())

def services_details(request,id):
    settings = cms_models.Settings.objects.first()
    services = extra_models.OurServices.objects.get(id=id)
    return render(request, 'pages/details/service_detail.html', locals())

def team(request):
    settings = cms_models.Settings.objects.first()
    team = extra_models.Team.objects.all()
    return render(request, 'pages/base/team.html', locals())

def blog(request):
    settings = cms_models.Settings.objects.first()
    blogs = cms_models.Blog.objects.all()
    return render(request, 'pages/base/blog.html', locals())

def blog_details(request,id):
    settings = cms_models.Settings.objects.first()
    blog = cms_models.Blog.objects.get(id=id)
    return render(request, 'pages/details/blog-details.html', locals())