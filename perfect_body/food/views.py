from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse

from .models import FoodUser
from .decorators import login_required, annon_required
from .helper import *


def food(request):
    if request.method == "POST":
        food_name = request.POST.get('food')
        food_meal_time = request.POST.get('meal_time')
        crawl_food(food_name, food_meal_time)
        return HttpResponse("ВЗЕХМЕ ХРАНАТА!")
    return render(request, 'food.html', {})


@annon_required(redirect_url=reverse_lazy('profile'))
def home(request):
    return render(request, 'home.html', {})


@login_required(redirect_url=reverse_lazy('home'))
def profile(request):
    email = request.session['food_email']
    user = FoodUser.objects.get(email=email)

    name = user.name
    years = user.years
    weight = user.weight
    height = user.height
    BMI = user.BMI
    max_cal = user.max_cal
    password = request.POST.get('password')

    if request.POST:
        if request.POST.get('Change Password'):
            print(request.POST)

    return render(request, 'profile.html', locals())


def registration(request):
    if request.method == 'POST':
        name, email, password, gender, years, weight, height =\
            get_user_post_attr(request)

        if not FoodUser.exists(email):
            calc_BMI = int(weight) / ((int(height) / 100)**2)
            print(calculate_normal_BMI(int(years), calc_BMI))
            calc_cal = max_calories(int(height), int(weight), int(years), gender)
            u = FoodUser(
                name=name,
                email=email,
                password=password,
                gender=gender,
                years=years,
                weight=weight,
                height=height,
                BMI=calc_BMI,
                max_cal=calc_cal
            )
            u.save()

        else:
            error = "User already exists"
        return redirect(reverse('profile'))
    return render(request, 'register.html', locals())


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        u = FoodUser.login_user(email, password)

        if u is None:
            error = 'Wrong username or password'
        else:
            request.session['food_email'] = email
            return redirect(reverse('profile'))
    return HttpResponse(error)


def logout(request):
    request.session.flush()
    return redirect(reverse('home'))


def saveProfile(request):
    print(request.user)
    if request.POST:
        if request.user.check_password(request.POST.get("password")):
            return JsonResponse({'success': False})
        else:
            print(request.POST, request.user.email)
            FoodUser.objects.filter(email=request.user.email).update(password=request.POST.get("new_password"))

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
