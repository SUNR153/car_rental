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
    reviews = Review.objects.filter(author=request.user)
    return render(request, 'reviews/my_review.html', {'reviews': reviews})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

@login_required
def review_create(request, car_id=None):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            if car_id:
                review.car = Car.objects.get(pk=car_id)
            review.save()
            return redirect('reviews:review_list')
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_create.html', {'form': form})

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
    review = get_object_or_404(Review, pk=pk, author=request.user)  # Проверяем авторство
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:review_list')  # Исправлено на именованный URL
    return render(request, 'reviews/review_delete.html', {'review': review})
