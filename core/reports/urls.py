from django.urls import path
from core.reports.views import *

urlpatterns = [
  # Reports
  path('sale/', ReportSaleView.as_view(), name='sale_report'),
]