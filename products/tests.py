from django.test import TestCase
from accounts.models import Org
from categories.models import Category
from products.models import Product, UnitPrice
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import ipdb

# Create your tests here.


class ProductTestCase(TestCase):
    def setUp(self):
        self.org = baker.make_recipe('accounts.lhama_cafe')
        self.user = baker.make_recipe('accounts.gilairmay', org=self.org)
        self.token = Token.objects.get_or_create(user=self.user)[0]

        self.category = baker.make_recipe('categories.coffee', org=self.org)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_product_create(self):
        product_data = {'name': 'Espresso',
                        'category': self.category, 'org': self.org}

        product = Product.objects.create(**product_data)

        unit_price_data = {'product': product, 'value': 300}
        unit_price = UnitPrice.objects.create(**unit_price_data)

        self.assertEqual(product.name, product_data['name'])
        self.assertEqual(product.org, product_data['org'])
        self.assertEqual(product.category, product_data['category'])

        self.assertEqual(product.unitprice_set.last().value,
                         unit_price_data['value'])

    def test_product_create_view(self):

        product_data = {'category_id': self.category.id,
                        'name': 'latte', 'unitprice_value': 400}

        response = self.client.post(
            '/api/products/', product_data, format='json')

        product = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(product['name'], product_data['name'])
        self.assertEqual(product['unitprice']['value'],
                         product_data['unitprice_value'])

        self.assertEqual(product['category']['id'],
                         product_data['category_id'])

        self.assertEqual(len(Product.objects.all()), 1)

    def test_list_products(self):
        baker.make_recipe('products.latte',
                          category=self.category, org=self.org)

        baker.make_recipe('products.mocha', org=self.org,
                          category=self.category)

        baker.make_recipe('products.chai', org=self.org,
                          category=self.category)

        response = self.client.get('/api/products/')

        products = response.json()['products']

        self.assertEqual(len(products), 3)
