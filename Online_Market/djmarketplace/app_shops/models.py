from django.db import models
from django.shortcuts import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Title')

    class Meta:
        verbose_name_plural = 'Category'
        verbose_name = 'Category'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Shop(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Title')
    category = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = 'Shops'
        verbose_name = 'Shop'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('goods', args=[str(self.pk)])


class Good(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Title')
    description = models.CharField(max_length=150, blank=True, verbose_name='Description')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.PositiveIntegerField()
    bought = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Goods'
        verbose_name = 'Good'
        ordering = ('title',)

    def __str__(self):
        return self.title
