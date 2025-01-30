from django.contrib import admin
from .models import Food, Meal, DailyDiet, MealItem

class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_measurement', 'calories')
    search_fields = ('name',)  # Permite buscar por nombre
    list_filter = ('unit_measurement',)  # Filtro por unidad de medida

admin.site.register(Food, FoodAdmin)

class MealItemInline(admin.TabularInline):  # Permite agregar MealItems desde Meal
    model = MealItem
    extra = 1

class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_proteins', 'total_fats', 'total_carbohydrates', 'total_calories')
    inlines = [MealItemInline]
    readonly_fields = ('total_proteins', 'total_fats', 'total_carbohydrates', 'total_calories')

    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el método save_model para recalcular los totales
        cuando se guarde el modelo desde el admin.
        """
        obj.save()  # Llama al método save del modelo para calcular totales
        super().save_model(request, obj, form, change)

admin.site.register(Meal, MealAdmin)

class DailyDietAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_proteins', 'total_fats', 'total_carbohydrates', 'total_calories')
    filter_horizontal = ('meals',)  # Para seleccionar comidas fácilmente
    date_hierarchy = 'date'  # Navegación por fechas en la parte superior

admin.site.register(DailyDiet, DailyDietAdmin)
