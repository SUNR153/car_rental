from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .form import ReviewForm
from django.contrib import messages
from cars.models import Car
from users.models import User
from .form import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def my_review(request):
    review = Review.objects.filter(author=request.user)
    return render(request, 'reviews/my_review.html', {'reviews': review})

def review_list(request, car_id):
    review = Review.objects.filter(car_id=car_id)
    return render(request, 'reviews/review_list.html', {'reviews': review})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

@login_required
def review_create(request):
    car_id = request.GET.get('car_id')
    car = None
    if car_id:
        car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            if car:
                review.car = car
            review.save()
            if car:
                return redirect('cars:car_detail', pk=car.id)
            return redirect('reviews:review_list')
        else:
            print("Form errors:", form.errors)
    else:
        initial = {'car': car} if car else {}
        form = ReviewForm(initial=initial)
    return render(request, 'reviews/review_create.html', {'form': form, 'car': car})

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('reviews:review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/review_update.html', {
        'form': form,
        'review': review
    })

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, author=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:review_list')
    return render(request, 'reviews/review_delete.html', {'review': review})

