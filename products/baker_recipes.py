from model_bakery.recipe import Recipe
from .models import Product

latte = Recipe(Product, name='latte')
mocha = Recipe(Product, name='mocha')
chai = Recipe(Product, name='chai')
