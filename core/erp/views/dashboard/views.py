from django.db.models import Sum, FloatField
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from datetime import datetime

from core.erp.models import Sale, Product, DetailSale

from random import randint


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    # Usando AJAX para mostrar el gráfico
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Sobreescribir el método post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data = {
                    'name': 'Vendido',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_month()
                }
            elif action == 'get_graph_sales_products_year_moth':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_moth()
                }
            elif action == 'get_graph_live':
                data = {
                    'y': randint(1, 100)
                }
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_sales_products_year_moth(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Product.objects.all():
                total = DetailSale.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
                                                  product_id=p.id).aggregate(
                    r=Coalesce(Sum('quantity'), 0, output_field=FloatField())).get('r')
                if total > 0:
                    data.append({
                        'name': p.product_name,
                        'y': float(total),
                    })
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['subtitle'] = 'Gráfico de ventas'
        context['subtitleb'] = 'Gráfico de ventas utilizando AJAX'
        context['subtitlepie'] = 'Distribución porcentual de Ventas'
        context['subtitlelive'] = 'Gráfico Live'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context
