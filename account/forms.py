from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Plan
from django.core.exceptions import ValidationError
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.search(r'^[a-zA-Z0-9._]+$', username):
            raise ValidationError("Username can only contain letters, numbers, dots, and underscores.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            # Ensure a Plan instance exists before saving the User
            if not Plan.objects.filter(id=user.plan_id).exists():
                Plan.objects.create(id=user.plan_id, name='Default Plan', max_num_links=10, max_num_tag=10, max_num_catagory=10)
            user.save()

        return user

from django import forms

class ChangePlanForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['plan']
