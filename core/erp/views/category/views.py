from django.shortcuts import render
from django.urls import reverse_lazy

from core.erp.forms import CategoryForm
from core.erp.models import Category
from django.views.generic import ListView, CreateView


# Vistas basadas en funciones
def category_list(request):
  
  data = {
    'title': 'Categorías',
    'subtitle': 'Listado de categorías',
    'categories': Category.objects.all(),
  }

  return render(request, 'category/list.html', data)


# Vistas basadas en clases
class CategoryListView(ListView):
  model = Category
  template_name = 'category/list.html'

  # Enviamos un contexto para los títulos
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Categorías'
    context['subtitle'] = 'Lista de categorías'
    return context


class CategoryCreateView(CreateView):
  model = Category
  form_class = CategoryForm
  template_name = 'category/create.html'
  success_url = reverse_lazy('erp:category_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Nueva categoría'
    context['subtitle'] = 'Crear nueva categoría'
    return context