import json
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from weasyprint import HTML, CSS
from xhtml2pdf import pisa

from core.pos.forms import ClientForm, SaleForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import SaleProduct, Product, Sale, Client


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Sale.objects.all().order_by('-date_joined'):
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            elif action == 'search_details_prod':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id']):
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
        context['create_url'] = reverse_lazy('pos:sale_create')
        context['list_url'] = reverse_lazy('pos:sale_list')
        return context


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('pos:sale_list')
    permission_required = 'add_sale'
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
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(product_name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.product_name
                    # item['text'] = i.product_name  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])  # Llega como string, pero lo convertimos en listado
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(product_name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.product_name
                    item['text'] = i.product_name  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():  # Si en una parte del proceso ocurre un error, no se guardará nada en la base de datos
                    venta = json.loads(request.POST['sale'])
                    sale = Sale()
                    sale.date_joined = venta['date_joined']
                    sale.client_id = venta['client']
                    sale.subtotal = float(venta['subtotal'])
                    sale.iva = float(venta['iva'])
                    sale.total = float(venta['total'])
                    sale.save()

                    for i in venta['products']:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = i['id']
                        detail.quantity = int(i['quantity'])
                        detail.price = float(i['price'])
                        detail.subtotal = float(i['subtotal'])
                        detail.save()

                        detail.product.stock -= detail.quantity
                        detail.product.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(ci__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'create_cliente':
                with transaction.atomic():
                    form_client = ClientForm(request.POST)
                    data = form_client.save()
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
        context['form_client'] = ClientForm()
        return context


class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('pos:sale_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(product_name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.product_name
                    # item['text'] = i.product_name  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])  # Llega como string, pero lo convertimos en listado
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(product_name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    # item['value'] = i.product_name
                    item['text'] = i.product_name  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():  # Si en una parte del proceso ocurre un error, no se guardará nada en la base de datos
                    venta = json.loads(request.POST['sale'])
                    # sale = Sale.objects.get(pk=self.get_object().id) # Una forma de hacerlo
                    sale = self.get_object()
                    sale.date_joined = venta['date_joined']
                    sale.client_id = venta['client']
                    sale.subtotal = float(venta['subtotal'])
                    sale.iva = float(venta['iva'])
                    sale.total = float(venta['total'])
                    sale.save()
                    sale.saleproduct_set.all().delete()
                    for i in venta['products']:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = i['id']
                        detail.quantity = int(i['quantity'])
                        detail.price = float(i['price'])
                        detail.subtotal = float(i['subtotal'])
                        detail.save()

                        detail.product.stock -= detail.quantity
                        detail.product.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(ci__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'create_cliente':
                with transaction.atomic():
                    form_client = ClientForm(request.POST)
                    data = form_client.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in SaleProduct.objects.filter(sale_id=self.get_object().id):
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
        context['form_client'] = ClientForm()
        return context


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('pos:sale_list')
    permission_required = 'pos.delete_sale'
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


# xhtml2pdf
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
        return HttpResponseRedirect(reverse_lazy('pos:sale_list'))


# WeasyPrint
class SaleInvoicePdfWeasyPrintView(View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/factura.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {
                    'name': 'BEE ERP SRL',
                    'nit': '6238877011',
                    'address': 'Santa Cruz de la Sierra, Bolivia',
                },
                'logo': '{}{}'.format(settings.MEDIA_URL, 'logobee.png')
            }
            html_template = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/bootstrap-4.6.2/css/bootstrap.min.css')
            pdf = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('pos:sale_list'))
