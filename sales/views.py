from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import SaleSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Sale, SaleDetail
from categories.models import Category
from silk.profiling.profiler import silk_profile
from rest_framework.pagination import LimitOffsetPagination

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
# Create your views here.


class SaleListView(APIView, LimitOffsetPagination):
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

    @method_decorator(cache_page(60*10))
    @method_decorator(vary_on_headers('Autorization'))
    @silk_profile(name='Sale list')
    def get(self, request):
        queryset = Sale.objects.prefetch_related('saledetails__unitprice').prefetch_related(
            'saledetails__product__category').filter(paid=True, org=request.user.org)

        result_page = self.paginate_queryset(queryset, request, view=self)

        serializer = SaleSerializer(result_page, many=True)

        return Response({'sales': serializer.data})


class CategoryTotalView(APIView):
    def get(self, request):
        org = request.user.org
        totals = {}

        for category in Category.objects.all():
            category_total = 0
            saledetails = SaleDetail.objects.prefetch_related('unitprice').filter(
                product__category=category, sale__org=org)
            print(saledetails.explain(analyze=True, verbose=True))

            for saledetail in saledetails:
                category_total = category_total + saledetail.unitprice.value

            totals[category.name] = category_total

        return Response(totals)
