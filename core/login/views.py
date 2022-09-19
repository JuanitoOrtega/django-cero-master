from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView


# Create your views here.
class LoginFormView(LoginView):
  template_name = 'login.html'

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('erp:category_list')
    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Iniciar sesión'
    return context


class LoginFormularioView(FormView):
  form_class = AuthenticationForm
  template_name = 'login.html'
  success_url = reverse_lazy('erp:category_list')

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return HttpResponseRedirect(self.success_url)
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    login(self.request, form.get_user())
    return HttpResponseRedirect(self.success_url)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Iniciar sesión'
    return context


# Otra forma de cerrar sesión
class LogoutRedirectView(RedirectView):
  pattern_name = 'login'

  def dispatch(self, request, *args, **kwargs):
    logout(request)
    return super().dispatch(request, *args, **kwargs)