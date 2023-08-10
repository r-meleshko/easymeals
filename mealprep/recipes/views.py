from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import Ingredient, Recipe, RecipeIngredient, UserActiveRecipe, UserFavoriteRecipe, UserShoppingList


@api_view(['GET'])
def custom_handler404(request, exception):
    return render(request, 'recipes/404.html', status=404)


@api_view(['GET'])
@login_required
def index(request) -> redirect:
    """Redirect from index to active."""
    return redirect('recipes:active')


@api_view(['GET'])
@login_required
def choose(request) -> render:
    """List all available recipes sorted my meal type. Can be filtered by total preparation time or meal type."""
    recipes = Recipe.objects.all().order_by('meal_type')
    active_recipes = UserActiveRecipe.objects.filter(user_id=request.user.id).values_list('recipe', flat=True)
    favorite_recipes = UserFavoriteRecipe.objects.filter(user_id=request.user.id).values_list('recipe', flat=True)
    return render(request, 'recipes/choose.html',
                  {
                      'recipes': recipes,
                      'active_recipes': active_recipes,
                      'favorite_recipes': favorite_recipes,
                      'meal_types': recipes.order_by('meal_type').values_list('meal_type', flat=True).distinct(),
                      'prep_times': recipes.order_by('time_total').values_list('time_total', flat=True).distinct()
                  })


@api_view(['GET'])
@login_required
def active(request) -> render:
    """List of user active recipes."""
    recipes = UserActiveRecipe.objects.filter(user_id=request.user.id).select_related('recipe')
    favorite_recipes = UserFavoriteRecipe.objects.filter(user_id=request.user.id).values_list('recipe', flat=True)
    return render(
        request, 'recipes/active.html', {'recipes': recipes, 'favorite_recipes': favorite_recipes}
    )


@api_view(['GET'])
@login_required
def favorite(request) -> render:
    """List of user favorite recipes."""
    favorite_recipes = UserFavoriteRecipe.objects.filter(user_id=request.user.id).select_related('recipe')
    active_recipes = UserActiveRecipe.objects.filter(user_id=request.user.id).values_list('recipe', flat=True)
    return render(
        request, 'recipes/favorite.html', {'favorite_recipes': favorite_recipes, 'active_recipes': active_recipes}
    )


@api_view(['GET'])
@login_required
def shopping(request) -> render:
    """List of ingredients to buy for active recipe(s). Sorted by ingredient category."""
    recipes_list = UserActiveRecipe.objects.filter(user_id=request.user.id).values_list('recipe_id', flat=True)
    ingredients = RecipeIngredient.objects.filter(recipe_id__in=recipes_list).select_related('ingredient')
    ingredients = ingredients.values(
        'ingredient_id', 'ingredient__ingredient_id_hash', 'ingredient__ingredient_name', 'ingredient__ingredient_class',
        'quantity_unit'
    ).order_by().annotate(quantity=Sum("quantity"))
    categories = ["Légumes", "Fruits", "Herbes", "Végétarien", "Conserves", "Graines et Pâtes", "Épices",
                  "Laitier", "Salades", "Pains", "Autre"]
    ingr_dict = {i: ingredients.filter(ingredient__ingredient_class=i) for i in categories if ingredients.filter(ingredient__ingredient_class=i)}
    bought_ingredients = UserShoppingList.objects.filter(user_id=request.user.id, status=1).values_list('ingredient_id', flat=True)
    return render(request, 'recipes/shopping.html', {
        'ingr_dict': ingr_dict, 'categories': categories, 'bought_ingredients': bought_ingredients
    })


@api_view(['GET'])
@login_required
def recipe(request, recipe_id: int) -> render:
    """Recipe page with description, list of ingredients and instructions."""
    recipe_dict = eval(get_object_or_404(Recipe, recipe_id=recipe_id).recipe_json)
    nutr_val_cat = ['Énergie (kJ)', 'Énergie (kcal)', 'Matières grasses', 'dont acides gras saturés',
                    'Glucides', 'dont sucres', 'Protéines', 'Sel']
    unit = ['kJ', 'kcal'] + ['g'] * 5
    nutr_val = zip(nutr_val_cat, recipe_dict['nutritional_val'], unit)
    active_recipes = UserActiveRecipe.objects.filter(user_id=request.user.id).values_list('recipe', flat=True)
    favorite_recipes = UserFavoriteRecipe.objects.filter(user_id=request.user.id).values_list('recipe', flat=True)
    return render(request, 'recipes/recipe.html',
                  {'recipe': recipe_dict,
                   'nutr_val': nutr_val,
                   'active_recipe': recipe_id in active_recipes,
                   'favorite_recipe': recipe_id in favorite_recipes
                   })


@api_view(['POST'])
@login_required
def shopping_update(request) -> HttpResponse:
    """Change status of an ingredient (bought/to buy)."""
    ingredient_id = int(request.POST['ingredient_id'])
    ingredient = get_object_or_404(Ingredient, ingredient_id=ingredient_id)
    status = int(request.POST['action'])
    if UserShoppingList.objects.filter(user_id=request.user.id, ingredient=ingredient).exists():
        UserShoppingList.objects.filter(user_id=request.user.id, ingredient=ingredient).update(
            status=status
        )
    else:
        UserShoppingList(user_id=request.user.id, ingredient=ingredient, status=status).save()
    return HttpResponse('Success.')


@api_view(['POST'])
@login_required
def favorite_active_update(request):
    """Add/remove a recipe from user active/favorites recipes. Set all ingredients status to 'not bought'
    Used in choose, active and favorite views."""
    models_dict = {'favorites': UserFavoriteRecipe, 'active': UserActiveRecipe}
    model = models_dict[request.POST['model']]
    recipe_id = request.POST['recipe_id']
    if request.POST['action'] == 'add':
        existing_recipes = model.objects.filter(user_id=request.user.id).values_list('recipe_id', flat=True)
        if int(recipe_id) not in existing_recipes:
            model(user_id=request.user.id, recipe_id=recipe_id).save()
    elif request.POST['action'] == 'remove':
        model.objects.filter(user_id=request.user.id).filter(recipe_id=recipe_id).delete()
    if request.POST['model'] == 'active':
        UserShoppingList.objects.filter(user_id=request.user.id).update(status=0)
    return HttpResponse('Success')
