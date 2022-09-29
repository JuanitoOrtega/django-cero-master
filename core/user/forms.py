from django.forms import *
from .models import User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'image']
        labels = {
            'email': 'Correo electrónico',
        }
        # exclude = ['groups', 'user_permissions', 'last_login', 'date_joined']
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                    'class': 'form-control',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese un usuario',
                    'class': 'form-control',
                }
            ),
            'email': TextInput(
                attrs={
                    'type': 'email',
                    'placeholder': 'Ingrese su correo electrónico',
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'password': TextInput(
                attrs={
                    'type': 'password',
                    'placeholder': 'Ingrese una contraseña',
                    'class': 'form-control',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data