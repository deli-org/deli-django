from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ProductSerializer
from rest_framework.response import Response
import ipdb
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from core.behaviors import Protected

# Create your views here.


class ProductList(Protected):

    def get(self, request):
        org = request.user.org
        queryset = Product.objects.filter(org=org)
        serializer = ProductSerializer(queryset, many=True)

        return Response({'products': serializer.data})

    def post(self, request):
        org = request.user.org

        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = request.data['name']
        unitprice_value = request.data['unitprice_value']
        category_id = request.data['category_id']

        product = Product.objects.create(
            org=org, category_id=category_id, name=name)

        product.unitprice_set.create(value=unitprice_value)
        # This would be the same thing as calling:
        ## UnitPrice.objects.create(product=product, value=unitprice_value)

        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
