from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView

from app_users.forms import RegistrationUserForm, BalanseEditForm
from app_users.models import Profile, Order
from cart.cart import Cart
import logging

# Create your views here.

logger = logging.getLogger(__name__)


class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'app_user/registration.html'

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data.get('password1')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        Profile.objects.create(
            user=user, first_name=first_name,
            last_name=last_name,
        )
        username = form.cleaned_data.get('username')
        authenticate_user = authenticate(username=username, password=password)
        # После регистарации сразу авторизируем пользователя
        login(self.request, authenticate_user)
        # После регистраиции добавляем пользователя в начальную группу
        return redirect('main')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'app_user/login.html'


    def get_success_url(self):
        logger.info('{first_name} {last_name} logged in'.format(
            first_name=self.request.user.profile.first_name,
            last_name=self.request.user.profile.last_name,
        ))
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('main')


class ProfileInfo(LoginRequiredMixin, TemplateView):
    template_name = 'app_user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order'] = Profile.objects.get(pk=self.request.user.profile.pk).order_set.select_related('good')

        return context


class BalanseEdit(FormView):
    template_name = 'app_user/balance.html'
    form_class = BalanseEditForm

    def form_valid(self, form):
        balance = form.cleaned_data['balance']
        user = self.request.user.profile
        user.balance = user.balance + balance
        logger.info('{first_name} {last_name} replenished the balance {balance}'.format(
            first_name=self.request.user.profile.first_name,
            last_name=self.request.user.profile.last_name,
            balance=balance
        ))

        user.save()
        return redirect('profile')


class OrderView(TemplateView):
    template_name = 'app_user/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cart = Cart(self.request)
        money = int(self.request.user.profile.balance) - int(cart.get_total_price())
        if not money < 0:
            user = self.request.user.profile
            user.balance = money
            for item in cart:
                quantity = int(item['product'].quantity) - item['quantity']
                if quantity > 0:
                    Order.objects.create(profile=self.request.user.profile,
                                         good=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                    item['product'].quantity = quantity
                    item['product'].bought += item['quantity']
                    item['product'].save()
                    logger.info('{first_name} {last_name} placed an order'.format(
                        first_name=self.request.user.profile.first_name,
                        last_name=self.request.user.profile.last_name,
                    ))
                else:
                    context['quantity'] = True
                    context['good'] = item['product']
                    return context
            user.save()
            cart.clear()
            return context
        context['money'] = abs(money)
        return context
