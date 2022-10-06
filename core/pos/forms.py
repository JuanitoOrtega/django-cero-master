from datetime import datetime
from django.forms import *

from core.pos.models import Category, Product, Client, Sale


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
        # exclude = ['user_updated', 'user_creation']
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
            # 'image': FileInput(
            #     attrs={
            #         'class': 'form-control-file',
            #     }
            # ),
            'stock': NumberInput(
                attrs={
                    'class': 'form-control',
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
            'birthdate': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'id': 'birthdate',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'data-toggle': 'datetimepicker',
                    'data-target': '#birthdate',
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
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
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


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.none()
        for form in self.visible_fields():
            # form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['client'].widget.attrs['autofocus'] = True
        # self.fields['date_joined'].widget.attrs['class'] = 'form-control'
        # self.fields['client'].widget.attrs['style'] = 'width: 100%'

        # Otra forma de agregrar atributos
        # self.fields['date_joined'].widget.attrs = {
        #     'class': 'form-control datetimepicker-input',
        #     'id': 'id_date_joined',
        #     'data-target': '#id_date_joined',
        #     'data-toggle': 'datetimepicker',
        # }
        self.fields['subtotal'].widget.attrs = {
            'readonly': True,
            'class': 'form-control',
        }
        self.fields['total'].widget.attrs = {
            'readonly': True,
            'class': 'form-control',
        }

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': Select(
                attrs={
                    'class': 'custom-select select2',
                    # 'style': 'width: 100%',
                }
            ),
            'iva': TextInput(
                attrs={
                    # 'type': 'number',
                    'class': 'form-control',
                }
            ),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker',
                }
            )
        }