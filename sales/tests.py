from django.test import TestCase
from .models import Sale, SaleDetail
from accounts.models import Org
from products.models import Product, UnitPrice
from categories.models import Category

import ipdb

# Create your tests here.


class SaleTestCase(TestCase):
    def setUp(self):
        org_data = {'name': 'Cafe test'}
        self.org = Org.objects.create(**org_data)

        self.assertEqual(self.org.name, org_data['name'])

        category_data = {'name': 'Coffee', 'org': self.org}
        self.category = Category.objects.create(**category_data)

        self.assertEqual(self.category.name, category_data['name'])
        self.assertEqual(self.category.org, category_data['org'])

        product_data = {'name': 'Espresso',
                        'category': self.category, 'org': self.org}

        product = Product.objects.create(**product_data)
        self.product = product

        unit_price_data = {'product': product, 'value': 300}
        unit_price = UnitPrice.objects.create(**unit_price_data)

        self.assertEqual(product.name, product_data['name'])
        self.assertEqual(product.org, product_data['org'])
        self.assertEqual(product.category, product_data['category'])

        self.assertEqual(product.unitprice_set.last().value,
                         unit_price_data['value'])

    def test_open_sale_with_no_products(self):
        sale_data = {'org': self.org, 'identifier': 'table1'}

        sale = Sale.objects.create(**sale_data)

        self.assertEqual(len(sale.saledetails.all()), 0)
        self.assertEqual(sale.paid, False)
        self.assertEqual(sale.payment_type, None)

    def test_open_sale_with_products(self):

        sale_data = {'org': self.org, 'identifier': 'table1'}
        sale = Sale.objects.create(**sale_data)

        sale_detail = {'product': self.product, 'amount': 1,
                       'discount': 0, 'unitprice': self.product.unitprice_set.last(), 'sale': sale}

        SaleDetail.objects.create(**sale_detail)

        self.assertEqual(len(sale.saledetails.all()), 1)
