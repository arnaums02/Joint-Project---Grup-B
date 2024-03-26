from django import forms
from .models import UserRoomStaff

class SignInForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    class Meta:
        model = UserRoomStaff
        fields = ['email', 'password']