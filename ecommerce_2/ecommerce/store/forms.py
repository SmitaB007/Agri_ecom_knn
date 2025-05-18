from django import forms
from .models import Contact,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email: ",widget=forms.TextInput(attrs={'class':' form-group', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="First name:", max_length=100, widget=forms.TextInput(attrs={'class':' form-group', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Name:", max_length=100, widget=forms.TextInput(attrs={'class':'form-group', 'placeholder':'Last Name'}))
     
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    
    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['class'] = ' form-group'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = ""

        self.fields['password1'].widget.attrs['class'] =' form-group'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Enter password:'
        self.fields['password1'].help_text = ""


        self.fields['password2'].widget.attrs['class'] = 'form-group'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Re-enter the password:'
        self.fields['password2'].help_text = ""








class contactus(forms.ModelForm):
    email = forms.CharField(label="Enter your Email",widget=forms.TextInput(attrs={'class':'form-control custom-input','placeholder':'Enter your email'}),required=True)
    message = forms.CharField(label="Enter your message",widget=forms.TextInput(attrs={'class':'form-control custom-input','placeholder':'Type here..','rows':4}),required=True)
    class Meta : 
        model = Contact
        fields = ('email','message')


class Update_details(UserChangeForm):
    password = None
    email = forms.EmailField(label="Enter email",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email ID'}))
    first_name = forms.CharField(label="Enter first name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label="Enter last name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
    
    def __init__(self,*args,**kwargs):
        super(Update_details,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Enter your username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


class Update_password(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1','new_password2']

    def __init__(self,*args,**kwargs):
      super(Update_password,self).__init__(*args,**kwargs)
      self.fields['new_password1'].widget.attrs['class'] = 'form-control'
      self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
      self.fields['new_password1'].label = 'Enter password'
      self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

      self.fields['new_password2'].widget.attrs['class'] = 'form-control'
      self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm password'
      self.fields['new_password2'].label = 'Re-enter the password'



class Update_info(forms.ModelForm):
    phone = forms.CharField(label="Enter phone number",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),required=True)
    address1 = forms.CharField(label="Enter address 1",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}),required=True)
    address2 = forms.CharField(label="Enter address 2 ",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}),required=True)
    city = forms.CharField(label="Enter city",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),required=True)
    state = forms.CharField(label="Enter state",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}),required=True)
    zipcode = forms.CharField(label="Enter zipcode",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode'}),required=True)
    country = forms.CharField(label="Enter country",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'country'}),required=True)
     
    class Meta:
        model = Profile
        fields = ('phone','address1','address2','city','state','zipcode','country')




