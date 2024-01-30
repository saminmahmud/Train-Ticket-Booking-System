from django.shortcuts import render, redirect
from .forms import StationForm
from django.contrib import messages

def Add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Station Added successfully😀')
            return redirect('home')  
    else:
        form = StationForm()
    
    return render(request, 'add_station.html', {'form': form})