# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=35)
    calories_per_serving = models.IntegerField()
    image = models.ImageField(upload_to='cook_app/images/ingredients', blank=True, null=True)

    def __str__(self):
        return self.ingredient_name

    class Meta:
        db_table = 'ingredient'


class IngredientList(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=True, null=True)
    measurement = models.CharField(max_length=10, blank=True, null=True)
    recipe = models.ForeignKey('Recipe', models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE)

    def __str__(self):
        return self.ingredient.ingredient_name + ' - ' + str(self.id)

    class Meta:
        db_table = 'ingredient_list'
        unique_together = (('id', 'recipe', 'ingredient'),)


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length=35)
    cooking_time = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='cook_app/images/recipes', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.dish_name

    class Meta:
        db_table = 'recipe'


class RecipeLine(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=35)
    discription = models.CharField(max_length=200)
    order_number = models.IntegerField()
    recipe = models.ForeignKey('Recipe', models.CASCADE, db_column='recipe')
    image = models.ImageField(upload_to='cook_app/images/lines', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'recipe_line'
