from django.db import models
from django.urls import reverse
from django.conf import settings

class RecipeAuthor(models.Model):
    Name = models.CharField(max_length=25, help_text='Author Name', blank=True)
    Org = models.CharField(max_length=25, help_text='Organization Name', blank=True) # can be null
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)."""
        return self.Name

# class RecipeIngredient(models.Field): # TODO: Maybe split this into 2 different ingredient models, one for a standard list of ingredients sitewide holding information about the ingredient and one for a user inventory that has fields local to users
#         """A typical class defining a model, derived from the Model class."""

#         # Fields
#         Name = models.CharField(max_length=20, help_text='Ingredient Name')
#         Quantity = models.IntegerField(help_text='Ingredient Amount')
#         Units = models.CharField(max_length=10, help_text='Ingredient Unit')
#         # DaysBeforeExpire = models.IntegerField(help_text='Days Before Ingredient Expires') TODO
#         # PurchaseDate = models.DateField(help_text='Day Ingredient Was Purchased') TODO

class RecipeModel(models.Model):
    """A typical class defining a model, derived from the Model class."""


    # Fields
    Name = models.CharField(max_length=20, help_text='Recipe Name')
    # use recipeObj.ingredients.create(Name=,Quantity=) to generate ingredients or recipeObj.ingredients.add(ingredientObj) to add existing ones
    Ingredients = models.JSONField(help_text='Recipe Ingredients')
    Author = models.ForeignKey(RecipeAuthor, help_text='Recipe Author', blank=True, on_delete=models.DO_NOTHING, null=True)
    Directions = models.CharField(max_length=999, help_text='Recipe Directions')
    img = models.ImageField(upload_to='images/', help_text='Recipe Image')
    # mealType = models.CharField(max_length=20, help_text='Type of Meal: entree, snack, bread, drink') # entree, snack, bread, drink
    MEALTYPES = (('e','Entree'), ('b','Bread'), ('s', 'Snack'), ('d', 'Drink'), ('t','Dessert'))
    mealtype = models.CharField(
        max_length=1,
        choices=MEALTYPES,
        blank=True,
        help_text='Type of Meal: entree, snack, bread, drink',
    )
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)."""
        return self.Name
    # …

    # Metadata
    class Meta:
        ordering = ['Name']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.Name
