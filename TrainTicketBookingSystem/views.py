from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from train.models import Train, Seat, Schedule
from station.models import Station
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@login_required
def home(request, category_slug = None):
    train = Train.objects.all()
    if category_slug is not None:
        category = Station.objects.get(slug = category_slug)
        train = Train.objects.filter(start_station  = category)
    schedule =  Schedule.objects.all()
    categories = Station.objects.all()
    return render(request, 'home.html', {'trains' : train, 'category' : categories, 'schedule' : schedule})
 


@user_passes_test(lambda user: not user.is_authenticated, login_url='home')
def index(request):
    return render(request, 'index.html')
 
def about_us(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Send message successfully😀')
        return redirect('contact')
    else:
        return render(request, 'contact.html')
