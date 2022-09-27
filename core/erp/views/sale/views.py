from django.db import transaction
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import DetailSale, Product, Sale

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all().order_by('-id'):
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetailSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ventas'
        context['subtitle'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        return context


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(product_name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # item['value'] = i.product_name
                    item['text'] = i.product_name # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'add':
                with transaction.atomic(): # Si en una parte del proceso ocurre un error, no se guardará nada en la base de datos
                    venta = json.loads(request.POST['sale'])
                    sale = Sale()
                    sale.date_joined = venta['date_joined']
                    sale.client_id = venta['client']
                    sale.subtotal = float(venta['subtotal'])
                    sale.iva = float(venta['iva'])
                    sale.total = float(venta['total'])
                    sale.save()

                    for i in venta['products']:
                        detail = DetailSale()
                        detail.sale_id = sale.id
                        detail.product_id = i['id']
                        detail.quantity = int(i['quantity'])
                        detail.price = float(i['price'])
                        detail.subtotal = float(i['subtotal'])
                        detail.save()
                    data = {'id': sale.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ventas'
        context['subtitle'] = 'Creación de una venta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['detail'] = []
        return context


class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(product_name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.product_name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic(): # Si en una parte del proceso ocurre un error, no se guardará nada en la base de datos
                    venta = json.loads(request.POST['sale'])
                    # sale = Sale.objects.get(pk=self.get_object().id) # Una forma de hacerlo
                    sale = self.get_object()
                    sale.date_joined = venta['date_joined']
                    sale.client_id = venta['client']
                    sale.subtotal = float(venta['subtotal'])
                    sale.iva = float(venta['iva'])
                    sale.total = float(venta['total'])
                    sale.save()
                    sale.detailsale_set.all().delete()
                    for i in venta['products']:
                        detail = DetailSale()
                        detail.sale_id = sale.id
                        detail.product_id = i['id']
                        detail.quantity = int(i['quantity'])
                        detail.price = float(i['price'])
                        detail.subtotal = float(i['subtotal'])
                        detail.save()
                    data = {'id': sale.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetailSale.objects.filter(sale_id=self.get_object().id):
                item = i.product.toJSON()
                item['quantity'] = i.quantity
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ventas'
        context['subtitle'] = 'Edición de una venta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['detail'] = json.dumps(self.get_details_product())
        return context


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.delete_sale'
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
        context['title'] = 'Ventas'
        context['subtitle'] = 'Eliminación de una Venta'
        context['list_url'] = self.success_url
        return context


class SaleInvoicePdfView(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/invoice_pdf.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {
                    'name': 'BEE ERP SRL',
                    'nit': '6238877011',
                    'address': 'Santa Cruz de la Sierra, Bolivia',
                },
                'logo': '{}{}'.format(settings.MEDIA_URL, 'logobee.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"' # Esta línea habilita la descarga automática de la factura
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:sale_list'))
