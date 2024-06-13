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


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}),
        label=''  # Eliminamos la etiqueta
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña'}),
        label=''  # Eliminamos la etiqueta
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'password_confirm']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
            'password_confirm': '',
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'client'
        if commit:
            user.save()
        return user