from django.db.models import Sum
from django.views.generic import ListView, DetailView, FormView

from app_shops.forms import DateForm
from cart.forms import CartAddProductForm
from app_shops.models import Shop, Good


class Main(ListView):
    template_name = 'app_shop/main.html'
    context_object_name = 'shops'

    def get_queryset(self):
        queryset = Shop.objects.prefetch_related('category')
        return queryset


class Goods(DetailView, FormView):
    model = Shop
    template_name = 'app_shop/goods.html'
    context_object_name = 'shops'
    success_url = 'goods'
    form_class = CartAddProductForm


class BestSellingItemView(FormView, ListView):
    template_name = 'app_shop/best_selling_item.html'
    form_class = DateForm
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.GET:
            form_date = self.form_class(self.request.GET)
            if form_date.is_valid():
                date = form_date.cleaned_data['date']
                queryset = Good.objects.filter(
                    order__created_at__gte=date
                ).annotate(quantity_sum=Sum('order__quantity')).order_by(
                    '-quantity_sum')[:8]
                return queryset
