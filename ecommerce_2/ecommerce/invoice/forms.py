from .models import product_review
from django import forms 

class Reviewform(forms.ModelForm):
    review = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','rows':4,'placeholder':'Type here...'}))
    rating= forms.IntegerField(min_value=1,max_value=5,label="Rating (1-5)")

    class Meta:
        model = product_review
        fields = ['rating','review']


