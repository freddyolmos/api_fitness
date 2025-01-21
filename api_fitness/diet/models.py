from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100)
    cuantity = models.FloatField()
    unit_measurement = models.CharField(max_length=20)
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()
    
    def __str__(self):
        return self.name
    
class Meal(models.Model):
    name = models.CharField(max_length=100)  # Ej: "Desayuno", "Colación 1"
    foods = models.ManyToManyField(Food, related_name="meals")
    total_proteins = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)
    total_carbohydrates = models.FloatField(default=0)
    total_calories = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total_proteins = sum(food.proteins for food in self.foods.all())
        self.total_fats = sum(food.fats for food in self.foods.all())
        self.total_carbohydrates = sum(food.carbohydrates for food in self.foods.all())
        self.total_calories = sum(food.calories for food in self.foods.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DailyDiet(models.Model):
    date = models.DateField()
    meals = models.ManyToManyField(Meal, related_name="daily_diets")
    total_proteins = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)
    total_carbohydrates = models.FloatField(default=0)
    total_calories = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total_proteins = sum(meal.total_proteins for meal in self.meals.all())
        self.total_fats = sum(meal.total_fats for meal in self.meals.all())
        self.total_carbohydrates = sum(meal.total_carbohydrates for meal in self.meals.all())
        self.total_calories = sum(meal.total_calories for meal in self.meals.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dieta del {self.date}"

