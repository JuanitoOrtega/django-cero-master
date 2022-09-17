from django.http import JsonResponse
# from django.shortcuts import render
from django.urls import reverse_lazy

from core.erp.forms import CategoryForm
from core.erp.models import Category
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


# Vistas basadas en clases
class CategoryListView(ListView):
  model = Category
  template_name = 'category/list.html'

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

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


class CategoryUpdateView(UpdateView):
  model = Category
  form_class = CategoryForm
  template_name = 'category/create.html'
  success_url = reverse_lazy('erp:category_list')

  # Si usáramos el método post
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  # Si usáramos el método post
  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'edit':
        form = self.get_form()
        data = form.save()
      else:
        data['error'] = 'No ha ingresado a ninguna opción'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Actualizar categoría'
    context['subtitle'] = 'Actualizar nueva categoría'
    context['list_url'] = reverse_lazy('erp:category_list')
    context['action'] = 'edit'
    return context


class CategoryDeleteView(DeleteView):
  model = Category
  template_name = 'category/delete.html'
  success_url = reverse_lazy('erp:category_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Eliminar categoría'
    context['subtitle'] = 'Eliminar una categoría'
    context['list_url'] = reverse_lazy('erp:category_list')
    return context