from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label=_('Логин'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label=_('Повтор пароля'), widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label=_('Имя'), widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label=_('Фамилия'), widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name')


class BalanseEditForm(forms.ModelForm):
    balance = forms.IntegerField(label='Replenishment', min_value=1)

    class Meta:
        model = Profile
        fields = ('balance',)


