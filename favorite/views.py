from django.shortcuts import redirect, get_object_or_404, render
from cars.models import Car
from .models import Favorite
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def add_to_favorites(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Favorite.objects.get_or_create(user=request.user, car=car)
    return redirect('cars:car_detail', pk=car_id)

@login_required
def remove_from_favorites(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    favorite = Favorite.objects.filter(user=request.user, car=car)
    if favorite.exists():
        favorite.delete()
    return redirect('cars:car_detail', pk=car_id)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorites_list.html', {'favorites': favorites})
