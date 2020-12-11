from django.urls import path
from .views import SaleListView, CategoryTotalView

urlpatterns = [
    path('sales/', SaleListView.as_view()),
    path('category-totals/', CategoryTotalView.as_view())
]
