from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import RecipeAuthor, RecipeModel

def recipes(request):
    """View function for recipes page of site."""

    recipes = RecipeModel.objects.all()

    # if request.method == 'POST':
    #     # Get the value of the button that was clicked
    #     button_value = request.POST.get("my_button")

    #     # Do something with the value of the button
    #     print(button_value)
    #     print('post')
    #     return HttpResponse("Hello World")


    context = {}
    recipeNameList = []
    recipeList = {}
    recipe = {}
    i=0
    # Create a list of buttons.
    buttons = []
    for r in recipes:
        recipeNameList.append(r.Name)
        D = list(r.Directions.strip('][').split(', '))
        I = []
        for key, val in r.Ingredients.items():
            val['Name'] = key
            I.append(val)
        recipe = {'Ingredients':I, 'Author':r.Author, 'Directions':D, 'Img':r.img, 'Mealtype':r.mealtype} # you should only need the list of names and then selecting one should do a lookup for it
        recipeList[r.Name] = recipe                                                                                   
        if i==0:
            context['First'] = r.Name
            i+=1
        buttons.append([r.Name, 'path/to/action'])
    context['NameList'] = recipeNameList
    context['List'] = recipeList


    
    # Create a scrollable container.
    scroll_container = ' <div id="scroll-container">'
    # Add the buttons to the scrollable container.
    for button in buttons:
        scroll_container += '<button class="button" href="#{0}", value="{1}">{1}</button>'.format(button[1], button[0])
    scroll_container += '</div>'

    context['scroll_container'] = scroll_container
    print(context)
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Recipes.html', context=context)

def login(request):
    return render(request, 'LogIn.html')
