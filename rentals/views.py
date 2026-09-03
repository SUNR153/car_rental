from django.shortcuts import render, get_object_or_404, redirect
from .models import Rental
from cars.models import Car
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from notifications.models import Notification

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
    car = rental.car
    return render(request, 'rentals/rental_detail.html', {'rental': rental, 'car': car})


@login_required
def rental_update(request, pk):
    rental = get_object_or_404(Rental, pk=pk)

    if request.user != rental.customer and request.user != rental.car.author:
        return HttpResponseForbidden("You do not have permission to edit this rental.")

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

@login_required
def rental_delete(request, pk):
    rental = get_object_or_404(Rental, pk=pk)

    if request.user != rental.customer and request.user != rental.car.author:
        return HttpResponseForbidden("You do not have permission to delete this rental.")

    if request.method == 'POST':
        rental.delete()
        return redirect('/rentals/')
    return render(request, 'rentals/rental_delete.html', {'rental': rental})

@login_required
def rental_create(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not car.available_dates.filter(start_date__lte=start_date, end_date__gte=end_date).exists():
            messages.error(request, "This car is not available for the selected dates.")
            return redirect('rentals:rental_create', car_id=car_id)

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

@login_required
def profile(request):
    today = timezone.now().date()

    Rental.objects.filter(customer=request.user, end_date__lt=today).delete()

    return render(request, 'users/profile.html', {'u': request.user})
