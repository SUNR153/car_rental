from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .form import CarForm, CarAvailabilityForm
from django.urls import reverse
from rentals.models import Rental
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

def car_list(request):
    today = timezone.now().date()

    rented_car_ids = Rental.objects.filter(
        start_date__lte=today, end_date__gte=today
    ).values_list('car_id', flat=True)

    available_cars = Car.objects.exclude(id__in=rented_car_ids)

    return render(request, 'cars/car_list.html', {'cars': available_cars})


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
