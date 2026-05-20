from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Company, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'get_full_name', 'active_company', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Контакты', {'fields': ('phone', 'avatar')}),
        ('Активная компания', {'fields': ('active_company',)}),
        ('Уведомления', {'fields': ('notify_sms', 'notify_email', 'notify_push', 'notify_telegram')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['active_company'].queryset = Company.objects.filter(user=obj)
        return form


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'business_type', 'inn', 'tax_system', 'tariff')
    search_fields = ('name', 'inn', 'user__email')
    list_filter = ('business_type', 'tax_system', 'tariff')
    raw_id_fields = ('user',)
