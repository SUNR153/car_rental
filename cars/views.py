from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .form import CarForm
from django.urls import reverse

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        # Получаем список id машин в избранном
        favorite_car_ids = request.user.favorites.all().values_list('car_id', flat=True)
        is_favorite = car.id in favorite_car_ids

    context = {
        'car': car,
        'is_favorite': is_favorite,
    }
    return render(request, 'cars/car_details.html', context)

def car_create(request):
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        car=form.save(commit=False)
        car.author=request.user
        car.save()
        return redirect('cars:car_list')
    return render(request, 'cars/car_create.html', {'form': form})

def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('cars:car_detail', pk=car.pk)  # Убедитесь в правильности namespace
    return render(request, 'cars/car_update.html', {'form': form, 'car': car})  # Добавлен car в контекст

def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('cars:car_list')
    return render(request, 'cars/car_delete.html', {'car': car})
