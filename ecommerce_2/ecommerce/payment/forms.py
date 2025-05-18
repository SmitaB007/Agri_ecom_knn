from .models import ShippingAddress
from django import forms 

class shipping_form(forms.ModelForm):
    shipping_fullname = forms.CharField(label="Enter Fullname",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'fullname'}),required=False)
    shipping_Address1 = forms.CharField(label="Enter Address",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Address'}),required=False)
    shipping_email  = forms.CharField(label="Enter Email" ,widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Email'}),required=False)
    shipping_zipcode = forms.CharField(label="Enter zipcode",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Zipcode'}),required=False)
    shipping_state = forms.CharField(label="Enter state",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'State'}),required=False)
     
    class Meta:
        model = ShippingAddress
        fields = ['shipping_fullname','shipping_Address1','shipping_email','shipping_zipcode','shipping_state']
        exclude = ['user',]

class paymentform(forms.Form):
    card_name =  forms.CharField(label="Enter Name:",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Name on card'}),required=True)
    card_number =  forms.CharField(label="Enter Card Number",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Card Number'}),required=True)
    card_exp_date =  forms.CharField(label="Enter Expiry Date",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Expiry date'}),required=True)
    card_cvv_number =  forms.CharField(label="Enter CVV number",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'CVV'}),required=True)
    card_address1 =  forms.CharField(label="Enter Address 1",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Billing Address 1'}),required=True)
    card_address2 =  forms.CharField(label="Enter Address 2",widget=forms.TextInput(attrs={'class':'form-container','placeholder':'Billing Address 2'}),required=True)