from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=50, unique=True)
    weight = models.FloatField()
    quantity = models.FloatField()
    calories = models.IntegerField()
    health_label = models.ManyToManyField('HealthLabel')
    diet_label = models.ManyToManyField('DietLabel')
    protein_in_grams = models.FloatField()
    fat_in_grams = models.FloatField()
    carbohydrate_in_grams = models.FloatField()
    meal_time = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class HealthLabel(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class DietLabel(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class FoodUser(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20, default=123)
    gender = models.CharField(max_length=1)
    years = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    BMI = models.FloatField(default=0)
    max_cal = models.FloatField(default=0)

    @classmethod
    def exists(cls, email):
        try:
            u = cls.objects.get(email=email)
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def login_user(cls, email, password):
        try:
            u = cls.objects.get(email=email, password=password)
            return u
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.email


class History(models.Model):
    email = models.ForeignKey(
        'FoodUser',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)
    foods = models.ForeignKey(
        'Food',
        on_delete=models.CASCADE)
