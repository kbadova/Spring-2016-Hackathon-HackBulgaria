from django.http import HttpResponse
from django.shortcuts import render
from .helper import crawl_food


def food(request):
    if request.method == "POST":
        food_name = request.POST.get('food')
        crawl_food(food_name)
        return HttpResponse("ВЗЕХМЕ ХРАНАТА!")
    return render(request, 'food.html', {})


def home(request):
    return render(request, 'home.html', {})


def profile(request):
    return render(request, 'profile.html', {})
