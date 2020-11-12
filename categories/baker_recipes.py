from model_bakery.recipe import Recipe
from .models import Category

coffee = Recipe(Category, name="Coffee")
