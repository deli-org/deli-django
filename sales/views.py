from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import SaleSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Sale, SaleDetail

# Create your views here.


class SaleListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SaleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        org = request.user.org
        paid = request.data['paid']
        identifier = request.data['identifier']

        sale = Sale.objects.create(org=org, paid=paid, identifier=identifier)

        for saledetail in request.data['saledetails']:

            SaleDetail.objects.create(
                sale=sale, product_id=saledetail['product_id'],
                unitprice_id=saledetail['unitprice_id'], amount=saledetail['amount'], discount=saledetail['discount'])

        serializer = SaleSerializer(sale)

        return Response(serializer.data)

    def get(self, request):
        queryset = Sale.objects.filter(paid=True, org=request.user.org)

        serializer = SaleSerializer(queryset, many=True)

        return Response({'sales': serializer.data})
