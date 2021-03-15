from .models import Ingredient, Recipe
from django.forms import ModelForm


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
