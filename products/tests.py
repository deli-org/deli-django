from django.test import TestCase
from accounts.models import Org
from categories.models import Category
from products.models import Product, UnitPrice
from model_bakery import baker
import ipdb

# Create your tests here.


class ProductTestCase(TestCase):
    def setUp(self):
        self.org = baker.make_recipe('accounts.lhama_cafe')

        self.category = baker.make_recipe('categories.coffee', org=self.org)
        ipdb.set_trace()

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
