from django.urls import path
from app_shops.views import Main, Goods, BestSellingItemView

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('<int:pk>/goods', Goods.as_view(), name='goods'),
    path('/best_item', BestSellingItemView.as_view(), name='best_item')
]