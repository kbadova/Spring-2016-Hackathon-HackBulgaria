from django.contrib import admin
from .models import Food, DietLabel, HealthLabel, FoodUser, History


class FoodAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'weight',
        'quantity',
        'calories',
        'meal_time'
    ]


admin.site.register(Food, FoodAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date',
        'foods'
    ]


admin.site.register(History, HistoryAdmin)


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
                    'BMI',
                    'max_cal')

admin.site.register(FoodUser, FoodUserAdmin)
