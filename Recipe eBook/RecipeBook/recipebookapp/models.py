from django.db import models
from django.urls import reverse

class RecipeIngredientModel(models.Model): # TODO: Maybe split this into 2 different ingredient models, one for a standard list of ingredients sitewide holding information about the ingredient and one for a user inventory that has fields local to users
    """A typical class defining a model, derived from the Model class."""

    # Fields
    Name = models.CharField(max_length=20, help_text='Ingredient Name')
    Quantity = models.IntegerField(help_text='Ingredient Amount')
    # DaysBeforeExpire = models.IntegerField(help_text='Days Before Ingredient Expires') TODO
    # PurchaseDate = models.DateField(help_text='Day Ingredient Was Purchased') TODO
    # …
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)."""
        return self.Name

class RecipeAuthor(models.Model):
    Name = models.CharField(max_length=25, help_text='Author Name')
    Org = models.CharField(max_length=25, help_text='Organization Name') # can be null

class RecipeModel(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    Name = models.CharField(max_length=20, help_text='Recipe Name')
    # use recipeObj.ingredients.create(Name=,Quantity=) to generate ingredients or recipeObj.ingredients.add(ingredientObj) to add existing ones
    Ingredients = models.ManyToManyField(RecipeIngredientModel, help_text='Recipe Ingredients')
    Directions = models.TextField(help_text='Recipe Directions')
    img = models.ImageField(upload_to='images/', help_text='Recipe Image')
    mealType = models.CharField(max_length=20, help_text='Type of Meal: entree, snack, bread, drink') # entree, snack, bread, drink
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
