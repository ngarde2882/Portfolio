from django.contrib import admin
from .models import RecipeIngredientModel, RecipeAuthor, RecipeModel
# Register your models here.
admin.site.register(RecipeIngredientModel)
admin.site.register(RecipeAuthor)
admin.site.register(RecipeModel)