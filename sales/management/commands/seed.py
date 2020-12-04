from django.core.management.base import BaseCommand
from accounts.models import Org
from accounts.models import User
from products.models import Product, UnitPrice
from categories.models import Category
from sales.models import Sale, SaleDetail
from datetime import datetime, timedelta
from faker import Faker
import csv
import os
import random

PATH = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_CSV = PATH + '/products.csv'


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        self.create_org_and_user()
        self.create_products_from_csv()
        self.create_sales_in_last_days(10)
        self.stdout.write('done!')

    def create_org_and_user(self):
        org, org_created = Org.objects.get_or_create(name="Lhama Café")
        if org_created:
            self.stdout.write(f'{org.name} created')
        else:
            self.stdout.write(f'{org.name} was already there')

        user = User.objects.filter(username='gilairmay')
        if not user:
            user = User.objects.create_user(
                username='gilairmay', password='1234', org=org)
            self.stdout.write(f'{user.username} created')
        else:
            self.stdout.write(f'{user[0].username} was already there')

        self.org = org

    def create_products_from_csv(self):
        with open(PRODUCTS_CSV) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            next(reader)
            for row in reader:
                print(str(row))
                category_name = row[0]

                category, category_created = Category.objects.get_or_create(
                    name=category_name, org=self.org)

                if category_created:
                    print(f'{category.name} created')
                else:
                    print(f'{category.name} was already there')

                product_name = row[2]

                product, product_created = Product.objects.get_or_create(
                    name=product_name, category=category, org=self.org)

                if product_created:
                    print(f'{product.name} created')
                else:
                    print(f'{product.name} was already there')

                unitprice_value = round(float(row[4])) * 100

                UnitPrice.objects.get_or_create(
                    value=unitprice_value, product=product)

    def create_sales_in_last_days(self, days):
        final_datetime = datetime.now()
        current_datetime = final_datetime - timedelta(days=days)

        # a gente itera sobre os dias
        # para cada dia, criamos um conjunto de vendas
        # ao final da iteração, adicionamos 1dia no current_datetime
        # o algoritmo para quando o current_datetime > hoje (final_datetime)
        while current_datetime < final_datetime:
            sales_in_day = random.choice(range(30, 50))

            for _ in range(1, sales_in_day):
                self.create_random_sale_between(
                    start_date=current_datetime.date(), end_date=current_datetime.date() + timedelta(days=1))

            current_datetime = current_datetime + timedelta(days=1)

    def create_random_sale_between(self, **kwargs):
        fake = Faker()
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']

        sale_created_at = fake.date_time_between(
            start_date=start_date, end_date=end_date)

        sale = Sale.objects.create(paid=True, payment_type='DEBIT',
                                   created_at=sale_created_at, updated_at=sale_created_at,
                                   org=self.org, identifier='table 1')

        product_list = self.select_random_products(10)
        for product in product_list:
            SaleDetail.objects.create(
                product=product, amount=1, unitprice=product.unitprice_set.last(), discount=0, sale=sale)

    def select_random_products(self, max):
        products = Product.objects.all()
        amount = random.choice(range(1, max))

        random_products = random.sample(list(products), amount)
        return random_products
