# Generated by Django 3.1.3 on 2020-11-09 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_remove_product_price'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('payment_type', models.CharField(choices=[('DEBIT', 'debit'), ('CREDIT', 'credit'), ('CASH', 'cash')], max_length=6, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.org')),
            ],
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('discount', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saledetails', to='sales.sale')),
                ('unitprice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.unitprice')),
            ],
        ),
    ]
