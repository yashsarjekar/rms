# recipes/serializers.py
from rest_framework import serializers
from .models import Ingredient, Recipe

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'instructions', 'ingredients']
