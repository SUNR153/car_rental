from django.shortcuts import render, get_object_or_404, redirect
from .models import Rental
from cars.models import Car
from users.models import User
from django.contrib import messages
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .form import RentalForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

User = get_user_model()

def my_rental(request):
    if not request.user.is_authenticated:
        return render(request, 'rentals/my_rental.html', {'rentals': []})
    rentals = Rental.objects.filter(customer=request.user)
    return render(request, 'rentals/my_rental.html', {'rentals': rentals})

def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, 'rentals/rental_list.html', {'rentals': rentals})

def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    return render(request, 'rentals/rental_detail.html', {'rental': rental})

@login_required
def rental_create(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if not request.user.profile.driver_license:
        messages.error(request, "You must have a valid driver's license to rent a car.")
        return redirect('cars:car_detail', pk=car.pk)

    if request.method == 'POST':
        try:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if end < start:
                messages.error(request, 'The end date cannot be earlier than the start date.')
                return redirect('rentals:rental_create', car_id=car_id)
            
            Rental.objects.create(
                car=car,
                customer=request.user,
                start_date=start,
                end_date=end
            )
            
            if car.author != request.user:
                Notification.objects.create(
                    user=car.author,
                    message=f"{request.user.email} rented your car '{car.brand} {car.model}' from {start} to {end}."
            )

            messages.success(request, 'Rental successfully created!')
            return redirect('cars:car_detail', pk=car.pk)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('rentals:rental_create', car_id=car_id)

    return render(request, 'rentals/rental_create.html', {
        'car': car,
        'default_start': datetime.now().strftime('%Y-%m-%d'),
        'default_end': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    })


def rental_update(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    if request.method == 'POST':
        rental.car_id = request.POST['car']
        rental.customer_id = request.POST['customer']
        rental.start_date = request.POST['start_date']
        rental.end_date = request.POST['end_date']
        rental.total_price = request.POST['total_price']
        rental.save()
        return redirect(f'/rentals/{pk}/')
    cars = Car.objects.all()
    users = User.objects.all()
    return render(request, 'rentals/rental_update.html', {'rental': rental, 'cars': cars, 'users': users})

def rental_delete(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    if request.method == 'POST':
        rental.delete()
        return redirect('/rentals/')
    return render(request, 'rentals/rental_delete.html', {'rental': rental})

from notifications.models import Notification

def rental_create(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()

        if end < start:
            messages.error(request, 'The end date cannot be earlier than the start date.')
            return redirect('rentals:rental_create', car_id=car_id)

        rental = Rental.objects.create(
            car=car,
            customer=request.user,
            start_date=start,
            end_date=end
        )

        Notification.objects.create(
            user=request.user,
            message=f"You successfully rented {car.brand} {car.model}!"
        )

        Notification.objects.create(
            user=car.author,
            message=f"Your car {car.brand} {car.model} was rented!"
        )

        messages.success(request, 'Rental successfully created!')
        return redirect('cars:car_detail', pk=car.pk)

    return render(request, 'rentals/rental_create.html', {
        'car': car,
        'default_start': datetime.now().strftime('%Y-%m-%d'),
        'default_end': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    })

@login_required
def rental_extend(request, pk):
    rental = get_object_or_404(Rental, pk=pk)

    if request.user != rental.customer:
        return HttpResponseForbidden("You are not allowed to edit this rental.")

    if request.method == 'POST':
        try:
            start = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

            if end < start:
                messages.error(request, "End date cannot be before start date.")
            else:
                rental.start_date = start
                rental.end_date = end
                rental.total_price = (end - start).days * rental.car.price_per_day
                rental.save()
                messages.success(request, "Rental period updated.")
                return redirect('rentals:rental_detail', pk=rental.pk)

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, 'rentals/rental_extend.html', {'rental': rental})

@login_required
def owner_rentals(request):
    rentals = Rental.objects.filter(car__author=request.user).select_related('car', 'customer')
    return render(request, 'rentals/owner_rentals.html', {'rentals': rentals})