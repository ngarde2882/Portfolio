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
        D = list(r.Directions.strip('][').split(', '))
        I = []
        for key, val in r.Ingredients.items():
            val['Name'] = key
            I.append(val)
        recipe = {'Ingredients':I, 'Author':r.Author, 'Directions':D, 'Img':r.img, 'Mealtype':r.mealtype}
        recipeList[r.Name] = recipe
        # if i==0:
        #     context['First'] = {'Name':r.Name, 'Ingredients':I, 'Author':r.Author, 'Directions':D, 'Img':r.img, 'Mealtype':r.mealtype}
        #     i+=1
        if i==0:
            context['First'] = r.Name
            i+=1
    context['NameList'] = recipeNameList
    context['List'] = recipeList
    print(context)
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Recipes.html', context=context)

def login(request):
    return render(request, 'LogIn.html')
