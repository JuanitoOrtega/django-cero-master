from django.http import HttpResponseRedirect, JsonResponse
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

  # Sobreescribir el método post
  def post(self, request, *args, **kwargs):
    data = {}
    try:
      data = Category.objects.get(pk=request.POST['id']).toJSON()
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  # Enviamos un contexto para los títulos
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Categorías'
    context['subtitle'] = 'Lista de categorías'
    context['create_url'] = reverse_lazy('erp:category_create')
    return context


class CategoryCreateView(CreateView):
  model = Category
  form_class = CategoryForm
  template_name = 'category/create.html'
  success_url = reverse_lazy('erp:category_list')

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'add':
        form = self.get_form()
        # Alternativamente otra forma de usar post con ajax
        data = form.save()
        #if form.is_valid(False): # Si el error viene como objeto
        #  form.save(True) # Si el error viene como objeto
        # if form.is_valid(): # Si el error viene como string
        #  form.save() # Si el error viene como string
        # Alternativamente otra forma de usar post con ajax
        #else:
        #  data['error'] = form.errors
      else:
        data['error'] = 'No ha ingresado a ninguna opción'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Nueva categoría'
    context['subtitle'] = 'Crear nueva categoría'
    context['list_url'] = reverse_lazy('erp:category_list')
    context['action'] = 'add'
    return context