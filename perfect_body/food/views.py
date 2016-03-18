from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
import random
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

    breakfast_fields = Menu("breakfast")
    lunch_fields = Menu("lunch")
    dinner_fields = Menu("dinner")

    name, _, _, gender, years, weight, height, BMI, max_cal = get_cls_get_attr(FoodUser, request)
    if request.method == 'POST':
        pass
    if request.POST.get("Breakfast"):

        # name, _, _, gender, years, weight, height = get_user_post_attr(request)

        # BMI = int(weight) / ((int(height) / 100)**2)
        # calc_cal = max_calories(int(height), int(weight), int(years), gender)
        # new_password = request.POST.get('new_password')

        # new_food_user = FoodUser.objects.filter(name=name)\
        #                                 .update(password=new_password,
        #                                         years=years,
        #                                         weight=weight,
        #                                         height=height,
        #                                         BMI=BMI,
        #                                         max_cal=calc_cal)

        print(request.POST.getlist('checks[]'))
        get_quantity_of_food_breakfast(user, request.POST.getlist('checks[]'))
        return render(request, 'profile.html', locals())


    if request.POST.get("Lunch"):
        print(request.POST.getlist('checks[]'))

        return render(request, 'profile.html', locals())
    if request.POST.get("Dinner"):
        print(request.POST.getlist('checks[]'))

        return render(request, 'profile.html', locals())
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


def Menu(meal):
    foods = random.sample(set(Food.objects.filter(meal_time=meal)), 5)
    global FOOD_CHOICES
    FOOD_CHOICES = foods
    # print(FOOD_CHOICES)
    return foods


def get_quantity_of_food_breakfast(user, foods):
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
            if cal_per_food <= breakfast_calories - (foods_len-1)*30:
                foods_len -= 1
                breakfast_calories -= grams_per_food
                meal[food.name] = grams_per_food
                break
    print(meal)
    return meal
