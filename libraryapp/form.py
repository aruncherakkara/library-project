from django import forms
from .models import Book, Profile, Borrow
from django.contrib.auth.models import User
from dal import autocomplete

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class BorrowForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete'),
        label="Select User"
    )

    class Meta:
        model = Borrow
        fields = ['user', 'book', 'borrow_date', 'return_date']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'borrow_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }