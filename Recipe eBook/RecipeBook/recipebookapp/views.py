from django.shortcuts import render

# Create your views here.
from .models import RecipeAuthor, RecipeModel

def recipes(request):
    """View function for recipes page of site."""

    recipes = RecipeModel.objects.all()

    context = {}
    recipeNameList = []
    recipeList = {}
    recipe = {}
    i=0
    for r in recipes:
        recipeNameList.append(r.Name)
        recipe = {'Ingredients':r.Ingredients, 'Author':r.Author, 'Directions':r.Directions, 'Img':r.img, 'Mealtype':r.mealtype}
        recipeList[r.Name] = recipe
    context['NameList'] = recipeNameList
    context['List'] = recipeList
    print(context)
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Recipes.html', context=context)

def login(request):
    return render(request, 'LogIn.html')
