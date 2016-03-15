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
