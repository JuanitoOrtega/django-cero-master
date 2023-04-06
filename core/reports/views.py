from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.pos.models import Sale
from core.reports.forms import ReportForm


# Create your views here.
class ReportSaleView(FormView):
  template_name = 'sale/report.html'
  form_class = ReportForm

  # Sobreescribir el método post
  def post(self, request, *args, **kwargs):
      data = {}
      try:
          action = request.POST['action']
          if action == 'search':
              data = []
              start_date = request.POST.get('start_date', '')
              end_date = request.POST.get('end_date', '')
              queryset = Sale.objects.all()
              if len(start_date) and len(end_date):
                queryset = queryset.filter(date_joined__range=[start_date, end_date])
              for s in queryset:
                  # Enviamos los datos en formato array
                  data.append([
                      s.id,
                      s.client.first_name,
                      s.client.last_name,
                      s.date_joined.strftime('%Y-%m-%d'),
                      f'{s.subtotal:.2f}',
                      f'{s.total_iva:.2f}',
                      f'{s.total:.2f}',
                  ])
              subtotal = float(queryset.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('r'))
              iva = float(queryset.aggregate(r=Coalesce(Sum('iva'), 0, output_field=FloatField())).get('r'))
              total = float(queryset.aggregate(r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r'))

              data.append([
                  '',
                  '',
                  '',
                  '<b>TOTALES</b>',
                  f'{subtotal:.2f}',
                  f'{iva:.2f}',
                  f'{total:.2f}',
              ])
          else:
              data['error'] = 'Ha ocurrido un error.'
      except Exception as e:
          data['error'] = str(e)
      return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Reportes'
      context['subtitle'] = 'Reporte de Ventas'
      context['list_url'] = reverse_lazy('sale_report')
      return context
  