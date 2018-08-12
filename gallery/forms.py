from django.contrib.auth.models import User
from .models import Picture, Profile

from django.forms import (
    ModelForm, Textarea, TextInput, 
    EmailInput, SelectMultiple, CharField,
    PasswordInput,
    )

from django.core.exceptions import ValidationError

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', )


class CreatePictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
        widgets = {
            'title': TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Type your title here..', }, ),
            'description': Textarea(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Type your post here..', }, ),
            'category': SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'required': True, }, ),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class SignUpForm(ModelForm):
    password1 = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Confirm password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise ValidationError("Username already in use!")
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        return password2