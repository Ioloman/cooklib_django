from django.contrib import admin
from .models import Ingredient, IngredientList, Recipe, RecipeLine

admin.site.register(Ingredient)
admin.site.register(IngredientList)
admin.site.register(Recipe)
admin.site.register(RecipeLine)

