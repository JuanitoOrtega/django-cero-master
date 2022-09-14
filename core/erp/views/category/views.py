from django.shortcuts import render
from core.erp.models import Category
from django.views.generic import ListView


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
    context['subtitle'] = 'Lista dee categorías'
    return context