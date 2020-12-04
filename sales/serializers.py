from rest_framework import serializers
from .models import Sale, SaleDetail
from products.serializers import ProductSerializer
import ipdb


class SaleDetailSerializer(serializers.Serializer):
    # READ AND WRITE
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    unitprice_id = serializers.IntegerField()
    discount = serializers.IntegerField()

    # READ ONLY
    product = serializers.SerializerMethodField('get_product')

    def get_product(self, saledetail):
        product = saledetail.product
        return ProductSerializer(product).data


class SaleSerializer(serializers.Serializer):
    # READ AND WRITE
    saledetails = serializers.SerializerMethodField(
        'get_saledetails', read_only=False)
    identifier = serializers.CharField()
    paid = serializers.BooleanField()
    payment_type = serializers.CharField()

    def get_saledetails(self, sale):
        saledetails = sale.saledetails
        return SaleDetailSerializer(saledetails, many=True).data

    # READ ONLY
    id = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
