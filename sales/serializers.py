from rest_framework import serializers
from .models import Sale, SaleDetail


class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ('product_id', 'amount', 'unitprice_id', 'discount')


class SaleSerializer(serializers.ModelSerializer):
    saledetails = SaleDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Sale
        fields = ('paid', 'identifier', 'payment_type', 'saledetails')
