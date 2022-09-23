from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.forms import *
from core.erp.models import Product


class TestView(TemplateView):
    template_name = 'selectajax.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = []
                for i in Product.objects.filter(category_id=request.POST['id']):
                    data.append({'id': i.id, 'name': i.product_name})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Aninados'
        context['subtitle'] = 'Select Aninados | Django'
        context['form'] = SelectAjaxForm()
        return context


class Select2View(TemplateView):
    template_name = 'select2.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id': '', 'text': '---------'}]
                for i in Product.objects.filter(category_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.product_name})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Aninados'
        context['subtitle'] = 'Select Aninados | Django'
        context['form'] = Select2Form()
        return context


class AutoAjaxView(TemplateView):
    template_name = 'autoajax.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id': '', 'text': '---------'}]
                for i in Product.objects.filter(category_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.product_name})
            elif action == 'autocomplete':
                data = []
                for i in Category.objects.filter(name__icontains=request.POST['term'])[0:2]:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Autocompletado'
        context['subtitle'] = 'Autocompletado usando Ajax'
        context['form'] = AutoAjaxForm()
        return context


class AutoSelect2View(TemplateView):
    template_name = 'autoselect2.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id': '', 'text': '---------'}]
                for i in Product.objects.filter(category_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.product_name})
            elif action == 'autocomplete':
                data = []
                for i in Category.objects.filter(name__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Autocompletado'
        context['subtitle'] = 'Autocompletado usando Select2'
        context['form'] = AutoSelect2Form()
        return context