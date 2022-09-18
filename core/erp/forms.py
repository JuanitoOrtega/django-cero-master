from django.forms import *

from core.erp.models import Category


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Comentado para usar alternativamente widget_tweaks para dar estilo a los campos del formulario
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
    
    # Alternativamente otra forma de usar post con ajax
    # Comentado para no usar método post en UpdateView
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

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <= 3:
            raise forms.ValidationError('Validation xxx')
            # self.add_error('name', 'El nombre debe tener más de 3 caracteres.')
        return cleaned