from django.contrib.auth.models import AbstractUser
from django.db import models


BUSINESS_TYPE_CHOICES = [
    ('individual', 'Индивидуальный предприниматель'),
    ('llc', 'ООО'),
    ('jsc', 'АО'),
    ('other', 'Другое'),
]

BUSINESS_SIZE_CHOICES = [
    ('1', 'Менее 10 сотрудников'),
    ('2', '10–50 сотрудников'),
    ('3', '50–200 сотрудников'),
    ('4', '200–500 сотрудников'),
    ('5', '500–1000 сотрудников'),
    ('6', 'Более 1000 сотрудников'),
]

TAX_SYSTEM_CHOICES = [
    ('usn', 'УСН'),
    ('osno', 'ОСНО'),
    ('envd', 'ЕНВД'),
    ('patent', 'Патент'),
    ('eshn', 'ЕСХН'),
]

ACCOUNTING_PROGRAM_CHOICES = [
    ('1c', '1С'),
    ('sbis', 'СБИС'),
    ('kontur', 'Контур'),
    ('moe_delo', 'Моё дело'),
    ('other', 'Другое'),
]

REPORTING_SYSTEM_CHOICES = [
    ('sbis', 'СБИС'),
    ('kontur', 'Контур.Экстерн'),
    ('taxcom', 'Такском'),
    ('other', 'Другое'),
]

ACCOUNTANT_TYPE_CHOICES = [
    ('own', 'Собственный бухгалтер'),
    ('outsource', 'Аутсорсинг'),
    ('self', 'Самостоятельно'),
    ('none', 'Нет'),
]

DOCUMENT_RESPONSIBLE_CHOICES = [
    ('invoices', 'Накладные'),
    ('acts', 'Акты'),
    ('all', 'Все документы'),
    ('other', 'Другое'),
]

HR_PROGRAM_CHOICES = [
    ('1c_zup', '1С:ЗУП'),
    ('1c', '1С'),
    ('kontur', 'Контур.Персонал'),
    ('other', 'Другое'),
]

ENTERTAINMENT_EXPENSES_CHOICES = [
    ('frequent', 'Частые'),
    ('rare', 'Редкие'),
    ('none', 'Нет'),
]

TARIFF_CHOICES = [
    ('basic', 'Базовый'),
    ('business', 'Бизнес'),
    ('corporate', 'Корпоративный'),
]


class User(AbstractUser):
    phone = models.CharField('Телефон', max_length=20, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    notify_sms = models.BooleanField('SMS-уведомления', default=False)
    notify_email = models.BooleanField('Email-уведомления', default=True)
    notify_push = models.BooleanField('Push-уведомления', default=False)
    notify_telegram = models.BooleanField('Telegram-уведомления', default=False)
    active_company = models.ForeignKey(
        'Company',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='active_for_users',
        verbose_name='Активная компания',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email or self.username

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'.strip() or self.username


class Company(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='companies',
        verbose_name='Пользователь',
    )
    # Основное
    logo = models.ImageField('Логотип', upload_to='logos/', blank=True, null=True)
    name = models.CharField('Наименование компании', max_length=200, blank=True)
    business_type = models.CharField(
        'Тип бизнеса', max_length=20, choices=BUSINESS_TYPE_CHOICES, blank=True
    )
    business_size = models.CharField(
        'Размер бизнеса', max_length=5, choices=BUSINESS_SIZE_CHOICES, blank=True
    )
    tariff = models.CharField(
        'Тариф', max_length=20, choices=TARIFF_CHOICES, blank=True, default=''
    )
    # Реквизиты
    industry = models.CharField('Деятельность в России', max_length=200, blank=True)
    inn = models.CharField('ИНН', max_length=12, blank=True)
    kpp = models.CharField('КПП', max_length=9, blank=True)
    legal_address = models.CharField('Юридический адрес', max_length=500, blank=True)
    registration_date = models.DateField('Дата регистрации', null=True, blank=True)
    tax_system = models.CharField(
        'Система налогообложения', max_length=20, choices=TAX_SYSTEM_CHOICES, blank=True
    )
    # Детальная информация
    accounting_program = models.CharField(
        'Программа ведения бухгалтерии', max_length=20,
        choices=ACCOUNTING_PROGRAM_CHOICES, blank=True
    )
    reporting_system = models.CharField(
        'Система сдачи отчётности', max_length=20,
        choices=REPORTING_SYSTEM_CHOICES, blank=True
    )
    accountant_type = models.CharField(
        'Кто ведёт учёт', max_length=20, choices=ACCOUNTANT_TYPE_CHOICES, blank=True
    )
    # Банковские реквизиты
    banks = models.CharField('Список банков', max_length=300, blank=True)
    currencies = models.CharField('Валюты', max_length=100, blank=True, default='RUB')
    has_bank_client = models.BooleanField('Наличие банк-клиента', default=False)
    has_second_sign = models.BooleanField('Передача второй подписи', default=False)
    avg_payments_per_month = models.PositiveIntegerField(
        'Среднее кол-во платёжных поручений/мес', default=0
    )
    foreign_currency_operations = models.PositiveIntegerField(
        'Количество валютных операций (импорт/экспорт)', default=0
    )
    # Договорной документооборот
    contracts_count = models.PositiveIntegerField(
        'Количество договоров с покупателями и поставщиками', default=0
    )
    document_responsible = models.CharField(
        'Ответственные за оформление документов',
        max_length=20, choices=DOCUMENT_RESPONSIBLE_CHOICES, blank=True
    )
    non_resident_contracts = models.PositiveIntegerField(
        'Контракты с нерезидентами', default=0
    )
    # Таможенные операции
    has_customs = models.BooleanField('Таможенные операции', default=False)
    counterparty_reconciliation = models.CharField(
        'Частота сверок с контрагентами', max_length=200, blank=True
    )
    # Активы и имущество
    has_property = models.CharField(
        'Наличие склада, недвижимости, земли', max_length=300, blank=True
    )
    fixed_assets_count = models.PositiveIntegerField(
        'Количество основных средств и НМА', default=0
    )
    vehicles_count = models.PositiveIntegerField(
        'Автомобилей на балансе', default=0
    )
    # Корпоративные карты
    has_corporate_cards = models.BooleanField('Корпоративные карты', default=False)
    # Кадровый учёт и зарплата
    hr_program = models.CharField(
        'Программа для кадрового учёта',
        max_length=20, choices=HR_PROGRAM_CHOICES, blank=True
    )
    employees_count = models.PositiveIntegerField(
        'Количество сотрудников (штат + ГПХ)', default=0
    )
    separate_divisions_count = models.PositiveIntegerField(
        'Обособленные подразделения', default=0
    )
    # Дополнительные настройки
    entertainment_expenses = models.CharField(
        'Представительские расходы',
        max_length=20, choices=ENTERTAINMENT_EXPENSES_CHOICES, blank=True
    )
    business_trips_count = models.PositiveIntegerField(
        'Командировки в месяц', default=0
    )
    expense_reports_count = models.PositiveIntegerField(
        'Авансовые отчёты в месяц', default=0
    )
    # Управленческая отчётность
    needs_management_report = models.BooleanField('Управленческая отчётность', default=False)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name or f'Компания #{self.pk}'
