from django import forms
from .models import User, AUCTION_LISTINGS, CATALOG, COMMENT_SECTION
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

class listing_form(ModelForm):
    class Meta:
            model = AUCTION_LISTINGS
            fields='__all__' 
            exclude=('status', 'watchlist', 'owner', 'sold_to')
            widgets = {
                'title': forms.TextInput(attrs={'placeholder': "Jakes Bike"}),
                'description':forms.Textarea(attrs={'placeholder': 'Max 1000 words'}),
                'price': forms.NumberInput(attrs={'placeholder': '$15'})
            }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = reverse_lazy('create_listing')
            self.helper.add_input(Submit('submit', 'List'))
            

def auto_bidding_form(min_bid, list_id):
    class bidding_form(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = reverse_lazy('lists', args=[list_id])
            self.helper.add_input(Submit('submit', 'Bid'))
        bid = forms.DecimalField(required=True, max_digits=14, decimal_places=2, min_value=min_bid+0.1,
                                 widget=forms.NumberInput(attrs={'placeholder': '$'+str(min_bid+0.1)}))
    return bidding_form

class comment_form(ModelForm):
    class Meta:
        model = COMMENT_SECTION
        fields=['comment_content',]
   