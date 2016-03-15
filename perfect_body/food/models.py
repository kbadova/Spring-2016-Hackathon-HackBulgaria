from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=50)
    weight = models.FloatField()
    quantity = models.FloatField()
    calories = models.IntegerField()
