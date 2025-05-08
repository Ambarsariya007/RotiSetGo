from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, NGOProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NGORegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = NGOProfile
        fields = [
            'organization_name',
            'registration_number',
            'address',
            'contact_person',
            'phone_number',
            'proof_document'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
    
    from django import forms
from .models import FoodListing
from django.utils import timezone

class FoodListingForm(forms.ModelForm):
    class Meta:
        model = FoodListing
        fields = ['food_type', 'quantity', 'description', 'expiry_date', 'pickup_location', 'pickup_time','image']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        if expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past")
        return expiry_date
    




    from django import forms
from .models import FoodRequest

class FoodRequestForm(forms.ModelForm):
    class Meta:
        model = FoodRequest
        fields = ['message', 'contact_info']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell the donor why you need this food...'
            }),
            'contact_info': forms.TextInput(attrs={
                'placeholder': 'Your phone number or email'
            })
        }