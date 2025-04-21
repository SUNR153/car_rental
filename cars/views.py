from django.shortcuts import render, get_object_or_404, redirect
from .models import Car

def car_list(request):
    car = Car.objects.all()
    return render(request, 'core/index.html', {'cars': car})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_details.html')

def car_create(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        model = request.POST['model']
        year = request.POST['year']
        price = request.POST['price_per_day']
        available = 'is_available' in request.POST
        Car.objects.create(
            brand=brand,
            model=model,
            year=year,
            price_per_day=price,
            is_available=available
        )
        return redirect('/cars/')
    return render(request, 'cars/car_create.html')

def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.brand = request.POST['brand']
        car.model = request.POST['model']
        car.year = request.POST['year']
        car.price_per_day = request.POST['price_per_day']
        car.is_available = 'is_available' in request.POST
        car.save()
        return redirect(f'/cars/{car.pk}/')
    return render(request, 'cars/car_update.html', {'cars': car})

def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('/cars/')
    return render(request, 'cars/car_delete.html', {'cars': car})
