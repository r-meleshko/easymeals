# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Concat
from django.db.models import Sum, Value
from django.db import models


# Recipe related tables
class Recipe(models.Model):

    class DifficultyType(models.TextChoices):
        FACILE = 'Facile'
        INTERMEDIAIRE = 'Intérmediaire'
        DIFFICILE = 'Difficile'

    recipe_id = models.AutoField(primary_key=True)
    recipe_id_hash = models.BigIntegerField()
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    time_total = models.SmallIntegerField()
    time_prep = models.SmallIntegerField()
    difficulty = models.CharField(max_length=20, choices=DifficultyType.choices)
    meal_type = models.CharField(max_length=50)
    recipe_json = models.CharField(max_length=10000)

    class Meta:
        managed = False
        db_table = 'recipe'

    def __str__(self):
        return f'{self.title} {self.subtitle}'


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_id_hash = models.BigIntegerField()
    ingredient_name = models.CharField(max_length=200)
    ingredient_class = models.CharField(max_length=200)
    ingredient_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ingredient'

    def __str__(self):
        return self.ingredient_name


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tag'

    def __str__(self):
        return f'{self.tag_name}'


class Tool(models.Model):
    tool_id = models.AutoField(primary_key=True)
    tool_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tool'

    def __str__(self):
        return f'{self.tool_name}'


class RecipeIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'recipe_ingredient'

    def __str__(self):
        return f'Recipe: {self.recipe}, ingredient: {self.ingredient}'


class RecipeNutrValue(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.RESTRICT, primary_key=True)
    energie_kj = models.FloatField()
    energie_kcal = models.FloatField()
    matieres_grasses = models.FloatField()
    acides_gras_satures = models.FloatField()
    glucides = models.FloatField()
    sucres = models.FloatField()
    proteines = models.FloatField()
    sel = models.FloatField()

    class Meta:
        managed = False
        db_table = 'recipe_nutr_value'


class RecipeTag(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)
    tag = models.ForeignKey('Tag', on_delete=models.RESTRICT)

    class Meta:
        managed = False
        db_table = 'recipe_tag'


class RecipeTool(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.RESTRICT)
    tool = models.ForeignKey(Tool, on_delete=models.RESTRICT)

    class Meta:
        managed = False
        db_table = 'recipe_tool'


# User related tables
class User(AbstractUser):
    pass


class UserShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(default=0)


class UserActiveRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)


class UserFavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)