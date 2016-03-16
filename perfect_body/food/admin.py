from django.contrib import admin
from .models import Food, DietLabel, HealthLabel, FoodUser


class FoodAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'weight',
        'quantity',
        'calories',
    ]


admin.site.register(Food, FoodAdmin)


class DietLabelAdmin(admin.ModelAdmin):
    list_display = [
        'tag'
    ]


admin.site.register(DietLabel, DietLabelAdmin)


class HealthLabelAdmin(admin.ModelAdmin):
    list_display = [
        'tag'
    ]


admin.site.register(HealthLabel, HealthLabelAdmin)


class FoodUserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'email',
                    'password',
                    'gender',
                    'years',
                    'weight',
                    'height',
                    'BMI',)

admin.site.register(FoodUser, FoodUserAdmin)
