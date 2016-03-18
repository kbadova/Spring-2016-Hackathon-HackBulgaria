from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
import random
from .models import *
from .decorators import login_required, annon_required
from .helper import *

from django.views.decorators.csrf import csrf_exempt


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

    breakfast_fields = Menu("breakfast")
    lunch_fields = Menu("lunch")
    dinner_fields = Menu("dinner")

    history = History.objects.filter(user=user).order_by('date')

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


def changePassword(request):
    email = request.session['food_email']
    if request.method == 'POST':
        if 'password' and 'new_password' in request.POST:
            new_password = request.POST.get('new_password')
            new_food_user = FoodUser.objects.filter(email=email)\
                                            .update(password=new_password)

            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def changeData(request):
    email = request.session['food_email']
    user = FoodUser.objects.get(email=email)
    if request.method == 'POST':
        if 'years' and 'weight' and 'height' in request.POST:
            new_years = request.POST.get('years')
            new_weight = request.POST.get('weight')
            new_height = request.POST.get('height')

            BMI = int(new_weight) / ((int(new_height) / 100)**2)
            max_cal = max_calories(int(new_height), int(new_weight), int(new_years), user.gender)

            new_food_user = FoodUser.objects.filter(email=email)\
                                            .update(years=new_years,
                                                    weight=new_weight,
                                                    height=new_height,
                                                    BMI=BMI,
                                                    max_cal=max_cal)
            return JsonResponse({"max_cal": max_cal, "BMI": BMI})
    return JsonResponse({"success": False})


@csrf_exempt
def breakfast(request):
    email = request.session['food_email']
    user = FoodUser.objects.get(email=email)
    if request.method == 'POST':
        if 'checks[]' in request.POST:

            data = get_quantity_of_food(user, request.POST.getlist('checks[]'))
            foods = request.POST.getlist('checks[]')
            for food_name in foods:
                food = Food.objects.get(name=food_name)
                History.objects.create(user=user, foods=food)
            return JsonResponse({"success": True, "data": data})
    return JsonResponse({"success": False})


@csrf_exempt
def lunch(request):
    email = request.session['food_email']
    user = FoodUser.objects.get(email=email)
    if request.method == 'POST':
        if 'checks[]' in request.POST:
            data = get_quantity_of_food(user, request.POST.getlist('checks[]'))
            foods = request.POST.getlist('checks[]')
            for food_name in foods:
                food = Food.objects.get(name=food_name)
                History.objects.create(user=user, foods=food)

            return JsonResponse({"success": True, "data": data})
    return JsonResponse({"success": False})


@csrf_exempt
def dinner(request):
    email = request.session['food_email']
    user = FoodUser.objects.get(email=email)
    if request.method == 'POST':
        if 'checks[]' in request.POST:
            data = get_quantity_of_food(user, request.POST.getlist('checks[]'))
            foods = request.POST.getlist('checks[]')
            for food_name in foods:
                food = Food.objects.get(name=food_name)
                History.objects.create(user=user, foods=food)
            return JsonResponse({"success": True, "data": data})
    return JsonResponse({"success": False})


def Menu(meal):
    foods = random.sample(set(Food.objects.filter(meal_time=meal)), 5)
    global FOOD_CHOICES
    FOOD_CHOICES = foods
    # print(FOOD_CHOICES)
    return foods


def get_quantity_of_food(user, foods):
    meal = {}
    filtered_foods = []
    breakfast_calories = (40 / 100.0) * user.max_cal
    print(breakfast_calories)
    foods_len = len(foods)
    for food_name in foods:
        item = Food.objects.get(name=food_name)
        filtered_foods.append(item)
    for food in filtered_foods:
        while True:
            grams_per_food = random.randrange(0, 400)
            print("cal za 100gr" + str(food.calories / 100.0) + "name" + str(food.name))
            cal_per_food = grams_per_food * (food.calories / 100.0)
            if cal_per_food <= breakfast_calories - (foods_len - 1) * 30:
                foods_len -= 1
                breakfast_calories -= grams_per_food
                meal[food.name] = grams_per_food
                break
    print(meal)
    return meal
