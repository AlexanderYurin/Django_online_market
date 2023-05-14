from django.contrib.auth.models import User
from django.db import models
import logging

from app_shops.models import Good

logger = logging.getLogger(__name__)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, verbose_name='Name')
    last_name = models.CharField(max_length=20, verbose_name='Surname')
    order_amount = models.IntegerField(default=0, verbose_name='Order amount')
    status = models.CharField(default='Bronze', max_length=50, verbose_name='Status')
    balance = models.IntegerField(default=0, verbose_name='Balance')

    class Meta:
        verbose_name_plural = 'Profiles'
        verbose_name = 'Profile'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_status(self):
        spent = sum(item.get_cost() for item in Order.objects.filter(profile__pk=self.pk))
        if spent > 1000:
            self.status = 'Silver'
            self.save()
        elif spent > 5000:
            self.status = 'Gold'
            self.save()
        if self.status != self.status:
            logger.info('{} {} changed status on {}'.format(
                self.user.profile.first_name,
                self.user.profile.last_name,
                self.status
            ))
        return self.status


class Order(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of order')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'

    def get_cost(self):
        return int(self.price * self.quantity)

    def __str__(self):
        return f'{self.pk}. {self.profile}: {self.good}'
