from django.urls import path
from .views import SaleListView

urlpatterns = [
    path('sales/', SaleListView.as_view())
]
