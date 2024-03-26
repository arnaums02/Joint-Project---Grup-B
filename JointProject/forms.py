from django import forms
from .models import UserRoomStaff

class SignInForm(forms.ModelForm):
    class Meta:
        model = UserRoomStaff
        fields = ['email', 'password']

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
        }