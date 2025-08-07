from django import forms
from .models import Book,Profile,Borrow
from django.contrib.auth.models import User

class bookform(forms.ModelForm):
    class Meta:
        model=Book
        fields='__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude=['user']

class BorrowForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Select Borrower"
    )

    class Meta:
        model = Borrow
        fields = ['user']
        