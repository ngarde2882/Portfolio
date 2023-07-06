from django.contrib import admin
from .models import RecipeAuthor, RecipeModel
# Register your models here.
admin.site.register(RecipeAuthor)
admin.site.register(RecipeModel)