from django.forms import *

from core.erp.models import Category


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Comentado para usar alternativamente widget_tweaks
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        # labels se puede omitir si en el modelos usamos verbose_name para cada columna de la tabla
        labels = {
            'name': 'Nombre:',
            'description': 'Descripción:'
        }
        widgets = {
            'name': TextInput(
                attrs = {
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese nombre para la categoría',
                    # 'autocomplete': 'off',
                }
            ),
            'description': Textarea(
                attrs = {
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese una breve descripción',
                    # 'autocomplete': 'off',
                    'rows': 3,
                    'cols': 3,
                }
            )
        }