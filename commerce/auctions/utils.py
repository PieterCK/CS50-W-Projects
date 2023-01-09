from django import forms
from .models import User, AUCTION_LISTINGS, CATALOG
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


categories = CATALOG.objects.all()
category_options = ()
for i in range(len(categories)):
    tmp = category_options+((i+1, str(categories[i])),)
    category_options = tmp


class listing_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('create_listing')
        self.helper.add_input(Submit('submit', 'List'))

    title = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'placeholder': "Jakes Bike"}))
    description = forms.CharField(max_length=1000, widget=forms.Textarea(
        attrs={'placeholder': 'Max 1000 words'}))
    image_url = forms.URLField(required=True)
    quantity = forms.IntegerField(required=True, min_value=1, initial=1)
    category = forms.ChoiceField(choices=category_options, required=True)
    price = forms.DecimalField(required=True, max_digits=14, decimal_places=2,
                               min_value=0.1, widget=forms.NumberInput(attrs={'placeholder': '$15'}))


def auto_bidding_form(min_bid, item_id):
    class bidding_form(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = ()
            self.helper.add_input(Submit('submit', 'Bid'))
        bid = forms.DecimalField(required=True, max_digits=14, decimal_places=2, min_value=min_bid+0.1,
                                 widget=forms.NumberInput(attrs={'placeholder': '$'+str(min_bid+1)}))
    return bidding_form
