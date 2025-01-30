from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit_measurement = models.CharField(max_length=20)
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()
    
    def __str__(self):
        return self.name
    
class Meal(models.Model):
    name = models.CharField(max_length=100)  # Ex: "Breakfast", "Snack 1"
    items = models.ManyToManyField(Food, through='MealItem', related_name='meals')  # Relación con el modelo intermedio
    total_proteins = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)
    total_carbohydrates = models.FloatField(default=0)
    total_calories = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # Guarda la instancia si es nueva para obtener un ID
        if not self.pk:
            super().save(*args, **kwargs)

        # Calcula los totales basados en los items
        self.total_proteins = sum(item.total_proteins for item in self.meal_items.all())
        self.total_fats = sum(item.total_fats for item in self.meal_items.all())
        self.total_carbohydrates = sum(item.total_carbohydrates for item in self.meal_items.all())
        self.total_calories = sum(item.total_calories for item in self.meal_items.all())

        # Guarda nuevamente con los valores actualizados
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class MealItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)  # Relación con Food
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_items')  # Relación con Meal
    quantity = models.FloatField()  # Cantidad personalizada

    # Propiedades calculadas
    @property
    def total_proteins(self):
        return self.quantity * (self.food.proteins )

    @property
    def total_fats(self):
        return self.quantity * (self.food.fats)

    @property
    def total_carbohydrates(self):
        return self.quantity * (self.food.carbohydrates)

    @property
    def total_calories(self):
        return self.quantity * (self.food.calories)

    def __str__(self):
        return f"{self.quantity} {self.food.unit_measurement} of {self.food.name} in {self.meal.name}"

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

