from rest_framework import serializers
from .models import Product, UnitPrice
from categories.serializers import CategorySerializer


class UnitPriceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('value', 'id')
        model = UnitPrice


class ProductSerializer(serializers.Serializer):
    # READ AND WRITE
    name = serializers.CharField()

    # WRITE ONLY
    unitprice_value = serializers.IntegerField(write_only=True)

    # READ-ONLY
    category = serializers.SerializerMethodField('get_category')
    unitprice = serializers.SerializerMethodField('get_unitprice')

    def get_category(self, product):
        category = product.category
        return CategorySerializer(category).data

    def get_unitprice(self, product):
        unit_price = product.unitprice_set.last()
        return UnitPriceSerializer(unit_price).data
