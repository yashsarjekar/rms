# recipes/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from django.core.paginator import Paginator

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

# Mutations for Ingredient
class CreateIngredient(graphene.Mutation):
    ingredient = graphene.Field(IngredientType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, name, description=None):
        ingredient = Ingredient(name=name, description=description)
        ingredient.save()
        return CreateIngredient(ingredient=ingredient)

class UpdateIngredient(graphene.Mutation):
    ingredient = graphene.Field(IngredientType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    def mutate(self, info, id, name, description=None):
        ingredient = Ingredient.objects.get(pk=id)
        ingredient.name = name
        ingredient.description = description
        ingredient.save()
        return UpdateIngredient(ingredient=ingredient)

class DeleteIngredient(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        ingredient = Ingredient.objects.get(pk=id)
        ingredient.delete()
        return DeleteIngredient(success=True)

# Mutations for Recipe
class CreateRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        title = graphene.String(required=True)
        instructions = graphene.String(required=True)
        ingredients = graphene.List(graphene.ID)

    def mutate(self, info, title, instructions, ingredients=None):
        recipe = Recipe(title=title, instructions=instructions)
        recipe.save()
        if ingredients:
            recipe.ingredients.set(ingredients)
        return CreateRecipe(recipe=recipe)

class AddIngredientInRecipe(graphene.Mutation):
    # Similar to CreateRecipe mutation
    recipe = graphene.Field(RecipeType)

    class Arguments:
        id = graphene.ID(required=True)
        ingredients = graphene.List(graphene.ID, required=True)

    def mutate(self, info, id, ingredients=None):
        recipe = Recipe.objects.get(
            id=id
        )
        new_ingredients = Ingredient.objects.filter(id__in=ingredients)
        if ingredients:
            recipe.ingredients.add(*new_ingredients)
            recipe.save()
        return AddIngredientInRecipe(recipe=recipe)

class DeleteIngredientFromRecipe(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        ingredients = graphene.List(graphene.ID, required=True)

    def mutate(self, info, id, ingredients=None):
        recipe = Recipe.objects.get(pk=id)
        new_ingredient_list = []
        if ingredients:
            ingredients_to_be_deleted = Ingredient.objects.filter(id__in=ingredients)
            recipe.ingredients.remove(*ingredients_to_be_deleted)
            recipe.save()
        return DeleteIngredientFromRecipe(success=True)

class PaginatedIngredientType(graphene.ObjectType):
    ingredients = graphene.List(IngredientType)
    total_pages = graphene.Int()
    has_next_page = graphene.Boolean()

# Queries for listing ingredients and recipes
class Query(graphene.ObjectType):
    all_ingredients = graphene.Field(
        PaginatedIngredientType, 
        search=graphene.String(), 
        first=graphene.Int(), 
        skip=graphene.Int(),
        page=graphene.Int(),
        page_size=graphene.Int(),
    )
    recipe_by_id = graphene.Field(RecipeType, id=graphene.ID(required=True))

    def resolve_all_ingredients(self,
        info, 
        search=None, 
        first=None, 
        skip=None, 
        page=1, 
        page_size=10
    ):
        qs = Ingredient.objects.all()
        if search:
            qs = qs.filter(name__icontains=search)
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]

        paginator = Paginator(qs, page_size)
        
        # Get the specified page
        try:
            ingredients = paginator.page(page)
        except Exception as err:
            ingredients = paginator.page(1)
        return PaginatedIngredientType(
            ingredients=ingredients.object_list,
            total_pages=paginator.num_pages,
            has_next_page=ingredients.has_next()
        )

    def resolve_recipe_by_id(self, info, id):
        return Recipe.objects.get(pk=id)

# Calculated field for ingredient count
class RecipeType(DjangoObjectType):
    ingredient_count = graphene.Int()

    class Meta:
        model = Recipe

    def resolve_ingredient_count(self, info):
        return self.ingredients.count()

class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()
    add_ingredient_in_recipe = AddIngredientInRecipe.Field()
    delete_ingredient_from_recipe =DeleteIngredientFromRecipe.Field()
    create_recipe = CreateRecipe.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
