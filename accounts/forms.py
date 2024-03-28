from django import forms

from accounts.models import CustomUser


class SignInForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
        }