from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import ClientForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Client


class ClientListView(ValidatePermissionRequiredMixin, ListView):
    model = Client
    template_name = 'client/list.html'
    permission_required = 'view_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                position = 1
                for i in Client.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['subtitle'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('client_create')
        context['list_url'] = reverse_lazy('client_list')
        return context


class ClientCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'add_client'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['subtitle'] = 'Creación un Cliente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ClientUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'change_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Edición un Cliente'
        context['title'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ClientDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'delete_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Eliminación de un Cliente'
        context['title'] = 'Clientes'
        context['list_url'] = self.success_url
        return context