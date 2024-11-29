from django.contrib import admin

# Register your models here.
from .models import Ingredient, Recipe

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'ingredient_count',)
    search_fields = ('title',)
    filter_horizontal = ('ingredients',)

    def ingredient_count(self, obj):
        return obj.ingredients.count()
    
    # Optional: Set a short description for the method (this will be the column name)
    ingredient_count.short_description = 'Number of Ingredients'

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)