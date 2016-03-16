from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse

from .models import User
from .decorators import login_required, annon_required
from .helpers import get_user_post_attr, calculate_normal_BMI


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', locals())


@annon_required(redirect_url=reverse_lazy('profile'))
def registration(request):
    if request.method == 'POST':
        name, email, password, gender, years, weight, height =\
            get_user_post_attr(request)

        if not User.exists(email):
            calc_BMI = int(weight)/((int(height)/100)**2)
            print(calculate_normal_BMI(int(years), calc_BMI))
            u = User(name=name,
                     email=email,
                     password=password,
                     gender=gender,
                     years=years,
                     weight=weight,
                     height=height,
                     BMI=calc_BMI)
            u.save()
        else:
            error = "User already exists"
        return redirect(reverse('home'))

    return render(request, 'registration.html', locals())


@login_required(redirect_url=reverse_lazy('profile'))
def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        u = User.login_user(email, password)

        if u is None:
            error = 'Wrong username or password'
        else:
            request.session['email'] = email
            return redirect(reverse('profile'))

    return render(request, 'login.html', locals())
