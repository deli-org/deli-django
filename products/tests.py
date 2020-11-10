from django.test import TestCase
from accounts.models import Org
from categories.models import Category
from products.models import Product, UnitPrice

# Create your tests here.


class ProductTestCase(TestCase):
    def setUp(self):
        org_data = {'name': 'Cafe test'}
        self.org = Org.objects.create(**org_data)

        self.assertEqual(self.org.name, org_data['name'])

        category_data = {'name': 'Coffee', 'org': self.org}
        self.category = Category.objects.create(**category_data)

        self.assertEqual(self.category.name, category_data['name'])
        self.assertEqual(self.category.org, category_data['org'])

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
