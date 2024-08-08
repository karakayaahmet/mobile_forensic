from django import forms
from django.forms import SelectMultiple

from phone_info.models import Phone


class PhoneCreateForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = 'phone_name', 'phone_model', 'phone_image', 'phone_isHome', 'phone_isActive', 'phone_isUpdated', 'phone_status', 'phone_os', 'phone_operator', 'phone_date'
        labels = {
            'phone_name': 'Phone Name',
            'phone_model': 'Phone Model',
            'phone_image': 'Phone Image',
            'phone_isHome': 'Is Home',
            'phone_isActive': 'Is Active',
            'phone_isUpdated': 'Is Updated',
            'phone_status': 'Phone Status',
            'phone_os': 'Phone OS',
            'phone_operator': 'Phone Operator',
            'phone_date': 'Phone Date'
        }
        widgets = {
            'phone_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_model': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_isHome': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_isActive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_isUpdated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_os': forms.Select(attrs={'class': 'form-control'}),
            'phone_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_operator': forms.Select(attrs={'class': 'form-control'}),
            'phone_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
        error_messages = {
            'phone_name': {
                'required': 'This field is required',
                'unique': 'This phone already exists',
                'max_length': 'This field is too long',
            },
            'phone_model': {
                'required': 'This field is required',
                'max_length': 'This field is too long'
            },
            'phone_image': {
                'required': 'This field is required',
            },
            'phone_isHome': {
                'required': 'This field is required'
            },
            'phone_isActive': {
                'required': 'This field is required'
            },
            'phone_isUpdated': {
                'required': 'This field is required'
            },
            'phone_os': {
                'required': 'This field is required'
            },
            'phone_status': {
                'required': 'This field is required'
            },
            'phone_operator': {
                'required': 'This field is required'
            },
            'phone_date': {
                'required': 'This field is required'
            }
        }


class PhoneEditForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = 'phone_name', 'phone_model', 'phone_image', 'phone_isHome', 'phone_isActive', 'phone_isUpdated', 'phone_status', 'phone_os', 'phone_operator', 'phone_date', 'categories'
        labels = {
            'phone_name': 'Phone Name',
            'phone_model': 'Phone Model',
            'phone_image': 'Phone Image',
            'phone_isHome': 'Is Home',
            'phone_isActive': 'Is Active',
            'phone_isUpdated': 'Is Updated',
            'phone_status': 'Phone Status',
            'phone_os': 'Phone OS',
            'phone_operator': 'Phone Operator',
            'phone_date': 'Phone Date',
        }
        widgets = {
            'phone_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_model': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_isHome': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_isActive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_isUpdated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone_os': forms.Select(attrs={'class': 'form-control'}),
            'phone_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_operator': forms.Select(attrs={'class': 'form-control'}),
            'phone_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'categories': SelectMultiple(attrs={'class': 'form-control'})
        }
        error_messages = {
            'phone_name': {
                'required': 'This field is required',
                'unique': 'This phone already exists',
                'max_length': 'This field is too long',
            },
            'phone_model': {
                'required': 'This field is required',
                'max_length': 'This field is too long'
            },
            'phone_image': {
                'required': 'This field is required',
            },
            'phone_isHome': {
                'required': 'This field is required'
            },
            'phone_isActive': {
                'required': 'This field is required'
            },
            'phone_isUpdated': {
                'required': 'This field is required'
            },
            'phone_os': {
                'required': 'This field is required'
            },
            'phone_status': {
                'required': 'This field is required'
            },
            'phone_operator': {
                'required': 'This field is required'
            },
            'phone_date': {
                'required': 'This field is required'
            }
        }
