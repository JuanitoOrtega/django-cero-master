from datetime import datetime
from django.forms import *

from core.erp.models import Category, Product, Client


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',
                }
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción para la categoría',
                    'class': 'form-control',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['product_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'product_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',
                }
            ),
            'category': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%;'
                }
            ),
            'image': FileInput(
                attrs={
                    'class': 'form-control-file',
                }
            ),
            'price': TextInput(
                attrs={
                    'type': 'number',
                    'step': '0.01',
                    'class': 'form-control',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'class': 'form-control',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                }
            ),
            'ci': TextInput(
                attrs={
                    'placeholder': 'Ingrese su CI',
                    'class': 'form-control',
                }
            ),
            'birthday': DateInput(format='%Y-%m-%d',
               attrs={
                   'value': datetime.now().strftime('%Y-%m-%d'),
                   'class': 'form-control',
               }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                    'class': 'form-control',
                }
            ),
            'gender': Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SelectAjaxForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control'
    }))


class Select2Form(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class AutoAjaxForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    search = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese una descripción'
    }))


class AutoSelect2Form(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))