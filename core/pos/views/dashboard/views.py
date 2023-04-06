from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from core.pos.models import Sale, Product, SaleProduct


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    # Sobreescribir el método post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                points = []
                year = datetime.now().year
                for m in range(1, 13):
                    total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    points.append(float(total))
                data = {
                    'name': 'Vendido',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': points
                }
            elif action == 'get_graph_sales_products_year_moth':
                points = []
                year = datetime.now().year
                month = datetime.now().month
                for p in Product.objects.filter():
                    total = SaleProduct.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month, product_id=p.id).aggregate(result=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('result')
                    if total > 0:
                        points.append({'name': p.name,'y': float(total)})
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': points
                }
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['subtitle'] = 'Gráfico de ventas'
        context['subtitleb'] = 'Gráfico de ventas utilizando AJAX'
        context['subtitlepie'] = 'Distribución porcentual de Ventas'
        context['subtitlelive'] = 'Gráfico Live'
        # context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context


def page_not_found404(request, exception):
    return render(request, '404.html')