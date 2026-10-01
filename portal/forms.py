from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Accounts
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=15, label="ім'я")
    secondname = forms.CharField(max_length=15, label="прізвище") 
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Accounts.objects.create(
                user = user,
                name = self.cleaned_data["name"],
                secondname = self.cleaned_data["secondname"],
                description = "",
            )
        return user

