from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from cars.models import Car
from users.models import User

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == 'POST':
        car_id = request.POST['car']
        user_id = request.POST['author']
        rating = request.POST['rating']
        comment = request.POST['comment']
        Review.objects.create(
            car_id=car_id,
            author_id=user_id,
            rating=rating,
            comment=comment
        )
        return redirect('/reviews/')
    cars = Car.objects.all()
    users = User.objects.all()
    return render(request, 'reviews/review_form.html', {'cars': cars, 'users': users})

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.car_id = request.POST['car']
        review.author_id = request.POST['author']
        review.rating = request.POST['rating']
        review.comment = request.POST['comment']
        review.save()
        return redirect(f'/reviews/{review.pk}/')
    cars = Car.objects.all()
    users = User.objects.all()
    return render(request, 'reviews/review_form.html', {'review': review, 'cars': cars, 'users': users})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('/reviews/')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
