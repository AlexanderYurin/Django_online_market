from django import forms


class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%d/%m/%Y'], help_text='day/mouth/year')


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')
