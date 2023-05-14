from django.contrib.auth.forms import UserCreationForm
from django import forms
from booking.models import Event, Review
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(
        attrs={"placeholder": "Username", "style": "border-radius: 15px;"}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password", "style": "border-radius: 15px;"}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', "placeholder": "Username", "style": "border-radius: 15px;"}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', "placeholder": "Email", "style": "border-radius: 15px;"}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', }),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', "placeholder": "Password", "style": "border-radius: 15px;"})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', "placeholder": "Confirm password", "style": "border-radius: 15px;"})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "event", "creator"]

    rating = forms.IntegerField(min_value=0, max_value=10)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["image"]


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=(("title", "Title"),), initial="title")

