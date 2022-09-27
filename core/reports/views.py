from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Sale
from core.reports.forms import ReportForm


# Create your views here.
class ReportSaleView(TemplateView):
  template_name = 'sale/report.html'

  @method_decorator(csrf_exempt)
  # @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)

  # Sobreescribir el método post
  def post(self, request, *args, **kwargs):
      data = {}
      try:
          action = request.POST['action']
          if action == 'search_report':
              data = []
              start_date = request.POST.get('start_date', '')
              end_date = request.POST.get('end_date', '')
              search = Sale.objects.all()
              if len(start_date) and len(end_date):
                search = search.filter(date_joined__range=[start_date, end_date])
              for s in search:
                  # Enviamos los datos en formato array
                  data.append([
                      s.id,
                      s.client.first_name,
                      s.client.last_name,
                      s.date_joined.strftime('%Y-%m-%d'),
                      format(s.subtotal, '.2f'),
                      format(s.iva, '.2f'),
                      format(s.total, '.2f'),
                  ])
              subtotal = float(search.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('r'))
              iva = float(search.aggregate(r=Coalesce(Sum('iva'), 0, output_field=FloatField())).get('r'))
              total = float(search.aggregate(r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r'))
              data.append([
                  '',
                  '',
                  '',
                  '<b>TOTALES</b>',
                  format(subtotal, '.2f'),
                  format(iva, '.2f'),
                  format(total, '.2f'),
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
      context['form'] = ReportForm()
      return context
  