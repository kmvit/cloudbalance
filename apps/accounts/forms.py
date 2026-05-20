from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import (
    ACCOUNTING_PROGRAM_CHOICES, ACCOUNTANT_TYPE_CHOICES,
    BUSINESS_SIZE_CHOICES, BUSINESS_TYPE_CHOICES,
    DOCUMENT_RESPONSIBLE_CHOICES, ENTERTAINMENT_EXPENSES_CHOICES,
    HR_PROGRAM_CHOICES, REPORTING_SYSTEM_CHOICES, TAX_SYSTEM_CHOICES,
    Company, User,
)


class RegisterForm(UserCreationForm):
    company_name = forms.CharField(
        label='Название компании', max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Название компании'}),
    )
    last_name = forms.CharField(
        label='Фамилия владельца', max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия владельца'}),
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта'}),
    )
    phone = forms.CharField(
        label='Телефон', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
    )
    business_type = forms.ChoiceField(
        label='Тип бизнеса',
        choices=[('', 'Выберите тип бизнеса')] + BUSINESS_TYPE_CHOICES,
    )
    business_size = forms.ChoiceField(
        label='Размер компании',
        choices=[('', 'Выберите размер')] + BUSINESS_SIZE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль'}),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )
    agree_terms = forms.BooleanField(
        label='Я согласен с условиями использования',
        required=True,
    )

    class Meta:
        model = User
        fields = ['last_name', 'email', 'phone', 'password1', 'password2', 'agree_terms']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            company = Company.objects.create(
                user=user,
                name=self.cleaned_data['company_name'],
                business_type=self.cleaned_data['business_type'],
                business_size=self.cleaned_data.get('business_size', ''),
            )
            user.active_company = company
            user.save(update_fields=['active_company'])
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
    )


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя', max_length=150, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        label='Фамилия', max_length=150, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'avatar',
            'notify_sms', 'notify_email', 'notify_push', 'notify_telegram',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
        }


class CompanyForm(forms.ModelForm):
    avg_payments_per_month = forms.IntegerField(
        label='Среднее количество платёжных поручений в месяц',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    foreign_currency_operations = forms.IntegerField(
        label='Количество валютных операций (импорт/экспорт)',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    contracts_count = forms.IntegerField(
        label='Количество договоров с покупателями и поставщиками',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    non_resident_contracts = forms.IntegerField(
        label='Контракты с нерезидентами',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    fixed_assets_count = forms.IntegerField(
        label='Количество основных средств и НМА',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    vehicles_count = forms.IntegerField(
        label='Автомобилей на балансе',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    employees_count = forms.IntegerField(
        label='Количество сотрудников (штат + ГПХ)',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    separate_divisions_count = forms.IntegerField(
        label='Обособленные подразделения',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    business_trips_count = forms.IntegerField(
        label='Инвестиционные командировки (количество в месяц)',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    expense_reports_count = forms.IntegerField(
        label='Авансовые отчёты (количество в месяц)',
        required=False, min_value=0, initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )

    def clean_avg_payments_per_month(self):
        return self.cleaned_data.get('avg_payments_per_month') or 0

    def clean_foreign_currency_operations(self):
        return self.cleaned_data.get('foreign_currency_operations') or 0

    def clean_contracts_count(self):
        return self.cleaned_data.get('contracts_count') or 0

    def clean_non_resident_contracts(self):
        return self.cleaned_data.get('non_resident_contracts') or 0

    def clean_fixed_assets_count(self):
        return self.cleaned_data.get('fixed_assets_count') or 0

    def clean_vehicles_count(self):
        return self.cleaned_data.get('vehicles_count') or 0

    def clean_employees_count(self):
        return self.cleaned_data.get('employees_count') or 0

    def clean_separate_divisions_count(self):
        return self.cleaned_data.get('separate_divisions_count') or 0

    def clean_business_trips_count(self):
        return self.cleaned_data.get('business_trips_count') or 0

    def clean_expense_reports_count(self):
        return self.cleaned_data.get('expense_reports_count') or 0

    class Meta:
        model = Company
        exclude = ['user', 'tariff']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Наименование компании'}),
            'logo': forms.FileInput(),
            'business_type': forms.Select(
                choices=[('', 'Выберите тип')] + BUSINESS_TYPE_CHOICES
            ),
            'business_size': forms.Select(
                choices=[('', 'Выберите размер')] + BUSINESS_SIZE_CHOICES
            ),
            'industry': forms.TextInput(attrs={'placeholder': 'Сфера деятельности'}),
            'inn': forms.TextInput(attrs={'placeholder': 'ИНН'}),
            'kpp': forms.TextInput(attrs={'placeholder': 'КПП'}),
            'legal_address': forms.TextInput(attrs={'placeholder': 'г. Москва, ул. ...'}),
            'registration_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'tax_system': forms.Select(choices=[('', 'Выберите систему')] + TAX_SYSTEM_CHOICES),
            'accounting_program': forms.Select(
                choices=[('', 'Выберите программу')] + ACCOUNTING_PROGRAM_CHOICES
            ),
            'reporting_system': forms.Select(
                choices=[('', 'Выберите систему')] + REPORTING_SYSTEM_CHOICES
            ),
            'accountant_type': forms.Select(
                choices=[('', 'Выберите вариант')] + ACCOUNTANT_TYPE_CHOICES
            ),
            'banks': forms.TextInput(attrs={'placeholder': 'Сбербанк, Альфа-банк...'}),
            'currencies': forms.TextInput(attrs={'placeholder': 'RUB, USD...'}),
            'avg_payments_per_month': forms.NumberInput(attrs={'placeholder': '0'}),
            'foreign_currency_operations': forms.NumberInput(attrs={'placeholder': '0'}),
            'contracts_count': forms.NumberInput(attrs={'placeholder': '0'}),
            'document_responsible': forms.Select(
                choices=[('', 'Выберите вариант')] + DOCUMENT_RESPONSIBLE_CHOICES
            ),
            'non_resident_contracts': forms.NumberInput(attrs={'placeholder': '0'}),
            'counterparty_reconciliation': forms.TextInput(attrs={'placeholder': 'Например: раз в квартал'}),
            'has_property': forms.TextInput(attrs={'placeholder': 'Склад, офис, земля...'}),
            'fixed_assets_count': forms.NumberInput(attrs={'placeholder': '0'}),
            'vehicles_count': forms.NumberInput(attrs={'placeholder': '0'}),
            'hr_program': forms.Select(
                choices=[('', 'Выберите программу')] + HR_PROGRAM_CHOICES
            ),
            'employees_count': forms.NumberInput(attrs={'placeholder': '0'}),
            'separate_divisions_count': forms.NumberInput(attrs={'placeholder': '0'}),
            'entertainment_expenses': forms.Select(
                choices=[('', 'Выберите вариант')] + ENTERTAINMENT_EXPENSES_CHOICES
            ),
            'business_trips_count': forms.NumberInput(attrs={'placeholder': '0'}),
            'expense_reports_count': forms.NumberInput(attrs={'placeholder': '0'}),
        }
