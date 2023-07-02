from django.shortcuts import render

# Create your views here.
from .models import RecipeIngredientModel, RecipeAuthor, RecipeModel

def recipes(request):
    """View function for recipes page of site."""

    recipes = RecipeModel.objects()

    context = {
        'recipes': recipes,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Recipes.html', context=context)
