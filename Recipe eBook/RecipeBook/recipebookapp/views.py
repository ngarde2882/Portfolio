from django.shortcuts import render

# Create your views here.
from .models import RecipeAuthor, RecipeModel

def recipes(request):
    """View function for recipes page of site."""

    recipes = RecipeModel.objects.all()

    context = {}
    context['Recipes'] = {}
    i=0
    for r in recipes:
        context['Recipes'][r.Name] = {'Ingredients':r.Ingredients, 'Author':r.Author, 'Directions':r.Directions['Directions'], 'Img':r.img, 'Mealtype':r.mealtype}
        i+=1
    # context['First'] = RecipeModel.objects.get(Users__contains=request.user.id)
    print(context)
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Recipes.html', context=context)
