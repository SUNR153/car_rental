from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .form import CarForm, CarAvailabilityForm
from django.urls import reverse
from rentals.models import Rental
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q

def car_list(request):
    today = timezone.now().date()

    Rental.objects.filter(end_date__lt=today).delete()

    rented_car_ids = Rental.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).values_list('car_id', flat=True)

    cars = Car.objects.exclude(id__in=rented_car_ids)

    brand = request.GET.get('brand')
    year = request.GET.get('year')
    fuel = request.GET.get('fuel')
    transmission = request.GET.get('transmission')
    seats = request.GET.get('seats')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if brand:
        cars = cars.filter(brand=brand)
    if year:
        cars = cars.filter(year=year)
    if fuel:
        cars = cars.filter(fuel_type=fuel)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if seats:
        cars = cars.filter(seats=seats)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)

    context = {
        'cars': cars,
        'brands': Car.objects.values_list('brand', flat=True).distinct(),
        'years': Car.objects.values_list('year', flat=True).distinct().order_by('year'),
        'fuel_types': Car.objects.values_list('fuel_type', flat=True).distinct(),
        'transmissions': Car.objects.values_list('transmission', flat=True).distinct(),
        'seats_list': Car.objects.values_list('seats', flat=True).distinct().order_by('seats'),
    }

    return render(request, 'cars/car_list.html', context)



def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        favorite_car_ids = request.user.favorites.all().values_list('car_id', flat=True)
        is_favorite = car.id in favorite_car_ids

    context = {
        'car': car,
        'is_favorite': is_favorite,
    }
    return render(request, 'cars/car_details.html', context)


@login_required
def car_create(request):
    car_form = CarForm(request.POST or None, request.FILES or None)
    availability_form = CarAvailabilityForm(request.POST or None)

    if request.method == 'POST':
        if car_form.is_valid() and availability_form.is_valid():
            car = car_form.save(commit=False)
            car.author = request.user
            car.save()

            availability = availability_form.save(commit=False)
            availability.car = car
            availability.save()

            messages.success(request, "Car and availability created successfully.")
            return redirect('cars:car_detail', pk=car.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'cars/car_create.html', {
        'form': car_form,
        'availability_form': availability_form
    })


@login_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.user != car.author:
        return HttpResponseForbidden("You do not have permission to edit this car.")

    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if form.is_valid():
        form.save()
        messages.success(request, "Car updated successfully.")
        return redirect('cars:car_detail', pk=car.pk)

    return render(request, 'cars/car_update.html', {'form': form, 'car': car})


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        messages.success(request, "Car deleted.")
        return redirect('cars:car_list')
    return render(request, 'cars/car_delete.html', {'car': car})


@login_required
def set_availability(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.user != car.author:
        return HttpResponseForbidden("You are not allowed to set availability for this car.")

    if request.method == 'POST':
        form = CarAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.car = car
            availability.save()
            messages.success(request, "Availability added successfully.")
            return redirect('cars:car_detail', pk=car.id)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = CarAvailabilityForm()

    return render(request, 'cars/set_availability.html', {'form': form, 'car': car})