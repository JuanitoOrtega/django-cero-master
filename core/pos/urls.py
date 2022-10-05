from django.urls import path
from core.pos.views.category.views import *
from core.pos.views.product.views import *
from core.pos.views.client.views import *
from core.pos.views.dashboard.views import *
from core.pos.views.tests.views import *
from core.pos.views.sale.views import *

app_name = 'pos'

urlpatterns = [
    # Category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # Client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # Product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # Sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfWeasyPrintView.as_view(), name='sale_invoice_pdf'),  # WeasyPrint
    # path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),  # xhtml2pdf
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Test
    path('selectajax/', TestView.as_view(), name='selectajax'),
    path('select2/', Select2View.as_view(), name='select2'),
    path('autoajax/', AutoAjaxView.as_view(), name='autoajax'),
    path('autoselect2/', AutoSelect2View.as_view(), name='autoselect2'),
    path('testemail/', TestEmailView.as_view(), name='testemail'),
]