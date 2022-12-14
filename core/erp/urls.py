from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.product.views import *
from core.erp.views.client.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.tests.views import *

app_name = 'erp'

urlpatterns = [
    # Category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/form/', CategoryFormView.as_view(), name='category_form'),
    # Product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # Client
    path('client/', ClientView.as_view(), name='client'),
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Test
    path('selectajax/', TestView.as_view(), name='selectajax'),
    path('select2/', Select2View.as_view(), name='select2'),
    path('autoajax/', AutoAjaxView.as_view(), name='autoajax'),
    path('autoselect2/', AutoSelect2View.as_view(), name='autoselect2'),
]