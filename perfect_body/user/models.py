from django.db import models


class User(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20, default=123)
    gender = models.CharField(max_length=1)
    years = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    BMI = models.FloatField(default=0)

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
