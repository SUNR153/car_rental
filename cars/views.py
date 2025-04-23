from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .form import CarForm
from django.urls import reverse

def car_list(request):
    car = Car.objects.all()
    return render(request, 'core/index.html', {'cars': car})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_details.html', {'car': car})

def car_create(request):
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('cars:list')
    return render(request, 'cars/car_create.html', {'form': form})

def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('cars:detail', pk=pk)
    return render(request, 'cars/car_update.html', {'form': form})

def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('cars:list')
    return render(request, 'cars/car_delete.html', {'car': car})
