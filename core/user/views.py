from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.user.forms import UserForm, UserProfileForm
from core.user.models import User


class UserListView(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'view_user'

    # Sobreescribir el método post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                position = 1
                for i in User.objects.all().order_by('-date_joined'):
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Enviamos un contexto para los títulos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['subtitle'] = 'Lista de usuarios'
        context['create_url'] = reverse_lazy('user_create')
        context['list_url'] = reverse_lazy('user_list')
        return context


class UserCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'add_user'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuario'
        context['subtitle'] = 'Crear nuevo usuario'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UserUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuario'
        context['subtitle'] = 'Editar usuario'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'delete_user'
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
        context['title'] = 'Usuario'
        context['subtitle'] = 'Eliminar usuario'
        context['list_url'] = self.success_url
        return context


class UserChooseGroup(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('dashboard'))

class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil'
        context['subtitle'] = 'Editar perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingresa tu contraseña actual'
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingresa tu nueva contraseña'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Vuelve a ingresar tu nueva contraseña'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)  # Para que la sesión no se cierre después de cambiar la contraseña
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuario'
        context['subtitle'] = 'Editar contraseña'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context