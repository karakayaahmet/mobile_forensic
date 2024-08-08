from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.contrib import messages

from django import forms


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username == 'ilker':
            messages.add_message(self.request, messages.SUCCESS, 'Hoşgeldin admin')

        return username

    # def confirm_login_allowed(self, user):
    #     if user.username.startswith('y'):
    #         raise forms.ValidationError('Bu kullanıcı adı ile giriş yapamazsınız')


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget = widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['password1'].widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirm'})
        self.fields['email'].required = True


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Bu email adresi ile daha önce kayıt olunmuş')

        return email



class UserChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password Confirm'})