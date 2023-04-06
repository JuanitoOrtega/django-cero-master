import json
import os

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, View
from weasyprint import HTML, CSS

from core.pos.forms import ClientForm, SaleForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import SaleProduct, Product, Sale, Client
from core.reports.forms import ReportForm


class SaleListView(ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_products_detail':
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
        context['create_url'] = reverse_lazy('sale_create')
        context['list_url'] = reverse_lazy('sale_list')
        return context


class SaleCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'add_sale'
    url_redirect = success_url

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
            elif action == 'search_products_select2':
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
                    products = json.loads(request.POST['products'])
                    sale = Sale()
                    sale.date_joined = request.POST['date_joined']
                    sale.client_id = int(request.POST['client'])
                    sale.iva = float(request.POST['iva'])
                    sale.save()
                    for i in products:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = int(i['id'])
                        detail.quantity = int(i['quantity'])
                        detail.price = float(i['price'])
                        detail.subtotal = detail.quantity * detail.price
                        detail.save()
                        detail.product.stock -= detail.quantity
                        detail.product.save()
                    sale.calculate_invoice()
                    data = {'id': sale.id}
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(ci__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    form = ClientForm(request.POST)
                    data = form.save()
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
        context['products'] = []
        context['form_client'] = ClientForm()
        return context


class SaleUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
        return form

    def get_details_product(self):
        data = []
        sale = self.get_object()
        for i in sale.saleproduct_set.all():
            item = i.product.toJSON()
            item['quantity'] = i.quantity
            data.append(item)
        print(data)
        return json.dumps(data)

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
            elif action == 'search_products_select2':
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
                    products = json.loads(request.POST['products'])
                    sale = Sale()
                    sale.date_joined = request.POST['date_joined']
                    sale.client_id = int(request.POST['client'])
                    sale.iva = float(request.POST['iva'])
                    sale.save()
                    for i in products:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = int(i['id'])
                        detail.quantity = int(i['quantity'])
                        detail.price = float(i['price'])
                        detail.subtotal = detail.quantity * detail.price
                        detail.save()
                        detail.product.stock -= detail.quantity
                        detail.product.save()
                    sale.calculate_invoice()
                    data = {'id': sale.id}
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(ci__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()  # Para buscar productos usando Select2
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    form = ClientForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ventas'
        context['subtitle'] = 'Edición de una venta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        context['form_client'] = ClientForm()
        return context


class SaleDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'delete_sale'
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


# WeasyPrint
class SaleInvoicePdfView(View):
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
        return HttpResponseRedirect(reverse_lazy('sale_list'))
