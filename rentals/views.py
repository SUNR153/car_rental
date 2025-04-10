from django.shortcuts import render, get_object_or_404, redirect
from .models import Rental
from cars.models import Car
from users.models import User

# Список всех аренд
def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, 'rentals/rental_list.html', {'rentals': rentals})

# Детали одной аренды
def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    return render(request, 'rentals/rental_detail.html', {'rental': rental})

# Создание аренды
def rental_create(request):
    if request.method == 'POST':
        car_id = request.POST['car']
        user_id = request.POST['customer']
        start = request.POST['start_date']
        end = request.POST['end_date']
        price = request.POST['total_price']
        Rental.objects.create(
            car_id=car_id,
            customer_id=user_id,
            start_date=start,
            end_date=end,
            total_price=price
        )
        return redirect('/rentals/')
    cars = Car.objects.all()
    users = User.objects.all()
    return render(request, 'rentals/rental_form.html', {'cars': cars, 'users': users})

# Редактирование аренды
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
    return render(request, 'rentals/rental_form.html', {'rental': rental, 'cars': cars, 'users': users})

# Удаление аренды
def rental_delete(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    if request.method == 'POST':
        rental.delete()
        return redirect('/rentals/')
    return render(request, 'rentals/rental_confirm_delete.html', {'rental': rental})
