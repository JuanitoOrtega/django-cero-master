from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Client
from core.erp.forms import ClientForm


class ClientView(TemplateView):
    template_name = 'client/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Client.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                client = Client()
                client.first_name = request.POST['first_name']
                client.last_name = request.POST['last_name']
                client.ci = request.POST['ci']
                client.birthday = request.POST['birthday']
                client.address = request.POST['address']
                client.gender = request.POST['gender']
                client.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['subtitle'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:client')
        context['form'] = ClientForm()
        return context
