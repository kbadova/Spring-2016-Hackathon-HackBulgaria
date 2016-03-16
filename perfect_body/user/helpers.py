def get_user_post_attr(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    years = request.POST.get('years')
    weight = request.POST.get('weight')
    height = request.POST.get('height')

    return name, email, password, gender, years, weight, height


NORMAL_BMI = {
    (19, 24): (19, 24),
    (25, 34): (20, 25),
    (35, 44): (21, 26),
    (45, 54): (22, 27),
    (55, 64): (23, 28),
    (65, 100): (24, 29),
}


def calculate_normal_BMI(years, bmi):
    for value in NORMAL_BMI.keys():
        current_bmi = NORMAL_BMI[value]
        if years >= value[0] and years <= value[1]\
           and bmi >= current_bmi[0] and bmi <= current_bmi[1]:
            return 'Your BMI is normal.'
        else:
            return 'Your BMI is not normal. Normal BMI is between {} and {}.'\
                  .format(current_bmi[0], current_bmi[1])
