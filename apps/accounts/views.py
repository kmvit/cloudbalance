from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetView as BasePasswordResetView,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View
from django.views.generic.edit import CreateView

from .forms import CompanyForm, LoginForm, ProfileForm, RegisterForm
from .models import Company, TARIFF_CHOICES


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Добро пожаловать! Регистрация прошла успешно.')
        return response


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'profile/index.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль обновлён.')
        return super().form_valid(form)


class CompanyView(LoginRequiredMixin, View):
    template_name = 'profile/company.html'

    def _get_active_company(self, request):
        user = request.user
        # Проверяем, что active_company принадлежит этому пользователю
        if user.active_company_id:
            try:
                return Company.objects.get(pk=user.active_company_id, user=user)
            except Company.DoesNotExist:
                pass
        # Берём первую компанию и делаем её активной
        company = Company.objects.filter(user=user).first()
        if company:
            user.active_company = company
            user.save(update_fields=['active_company'])
        return company

    def _context(self, request, form, company):
        return {
            'form': form,
            'object': company,
            'companies': Company.objects.filter(user=request.user),
        }

    def get(self, request, *args, **kwargs):
        company = self._get_active_company(request)
        form = CompanyForm(instance=company)
        return render(request, self.template_name, self._context(request, form, company))

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'switch':
            company = get_object_or_404(Company, pk=request.POST.get('company_id'), user=request.user)
            request.user.active_company = company
            request.user.save(update_fields=['active_company'])
            return redirect('company')

        if action == 'create':
            company = Company.objects.create(user=request.user)
            request.user.active_company = company
            request.user.save(update_fields=['active_company'])
            return redirect('company')

        company = self._get_active_company(request)
        import sys
        print('FILES:', request.FILES, file=sys.stderr)
        form = CompanyForm(request.POST, request.FILES, instance=company)
        print('VALID:', form.is_valid(), 'ERRORS:', form.errors, file=sys.stderr)
        if form.is_valid():
            saved = form.save(commit=False)
            saved.user = request.user
            saved.save()
            if not request.user.active_company:
                request.user.active_company = saved
                request.user.save(update_fields=['active_company'])
            messages.success(request, 'Данные компании обновлены.')
            return redirect('company')

        return render(request, self.template_name, self._context(request, form, company))


class ServicesView(LoginRequiredMixin, View):
    template_name = 'profile/services.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        tariff = request.POST.get('tariff', '')
        if tariff in dict(TARIFF_CHOICES):
            company = request.user.active_company
            if company and company.user == request.user:
                company.tariff = tariff
                company.save(update_fields=['tariff'])
                messages.success(request, 'Тариф успешно выбран.')
        return redirect('services')


class PasswordResetView(BasePasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
