import requests
from .models import Food, HealthLabel, DietLabel


def crawl_food(food_name):
    payload = {'app_id': '10a834bf', 'app_key': '60a214d2bced63520a7dc3e77f7557f4', 'ingr': food_name}
    r = requests.get('https://api.edamam.com/api/nutrition-data', params=payload)
    # if r.status_code != 200:
    #     raise "Request failed!"
    result = r.json()
    # if 'parsed' not in result['ingredients'][0].keys():
    #     raise "Food not found"
    food_parsed_name = result['ingredients'][0]['parsed'][0]['foodMatch']
    food_weight = result['ingredients'][0]['parsed'][0]['weight']
    food_quantity = result['ingredients'][0]['parsed'][0]['quantity']
    food_calories = result['calories']

    food_protein_in_grams = result['ingredients'][0]['parsed'][0]['nutrients']['PROCNT']['quantity']
    food_protein_in_grams = round(food_protein_in_grams, 2)
    food_fat_in_grams = result['ingredients'][0]['parsed'][0]['nutrients']['FAT']['quantity']
    food_fat_in_grams = round(food_fat_in_grams, 2)
    food_carbohydrate_in_grams = result['ingredients'][0]['parsed'][0]['nutrients']['CHOCDF']['quantity']
    food_carbohydrate_in_grams = round(food_carbohydrate_in_grams, 2)

    health_label = result['healthLabels']
    diet_label = result['dietLabels']

    health_objects = []
    diet_objects = []

    for diet_tag in diet_label:
        if not DietLabel.objects.filter(tag=diet_tag):
            obj = DietLabel.objects.create(tag=diet_tag)
            diet_objects.append(obj)

    for health_tag in health_label:
        if not HealthLabel.objects.filter(tag=health_tag):
            obj = HealthLabel.objects.create(tag=health_tag)
            health_objects.append(obj)

    if not Food.objects.filter(name=food_parsed_name):
        food = Food.objects.create(
            name=food_parsed_name,
            weight=food_weight,
            quantity=food_quantity,
            calories=food_calories,
            protein_in_grams=food_protein_in_grams,
            fat_in_grams=food_fat_in_grams,
            carbohydrate_in_grams=food_carbohydrate_in_grams,
        )

        for health_obj in health_objects:
            food.health_label.add(health_obj)
            food.save()

        for diet_obj in diet_objects:
            food.diet_label.add(diet_obj)
            food.save()
