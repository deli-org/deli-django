from model_bakery.recipe import Recipe
from .models import Org, User

lhama_cafe = Recipe(Org, name="Lhama Café")
gilairmay = Recipe(User, username='gilairmay', password='1234')
