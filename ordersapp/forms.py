from django import forms

from ordersapp.models import Order, OrderItem
from mainapp.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = 'test field help'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = 'test field help_2'
        #    uncomment to improve performance - reduce number of requests to DB
        # self.fields['product'].queryset = Product.get_items().select_related() # if uncomment appears an error fro get_items
