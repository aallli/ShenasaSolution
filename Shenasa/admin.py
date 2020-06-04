from django.contrib import admin
from django.contrib import messages
from jalali_date import datetime2jalali
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from Shenasa.models import LegalPerson, NaturalPerson, Role, PersonRole, News
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fields = ['name', 'active', ]
    list_display = ['name', 'active', ]
    model = NaturalPerson
    list_filter = ['active']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        try:
            super(RoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(PersonRole)
class PersonRoleAdmin(admin.ModelAdmin):
    fields = ['person', 'role', ]
    list_display = ['person', 'role', ]
    model = PersonRole

    def save_model(self, request, obj, form, change):
        try:
            super(PersonRoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(News)
class NewsAdmin(ModelAdminJalaliMixin, SummernoteModelAdmin):
    summernote_fields = ('description',)
    fields = ['description', 'link', 'date', ]
    list_display = ['title', 'get_created_jalali']
    model = News

    class Media:
        css = {'all': ('css/custom_admin.css',)}
        js = ('js/custom_admin.js',)

    def save_model(self, request, obj, form, change):
        try:
            super(NewsAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date).strftime('%y/%m/%d _ %H:%M:%S')

    get_created_jalali.short_description = _('Creation Date')
    get_created_jalali.admin_order_field = 'date'


@admin.register(NaturalPerson)
class NaturalPersonAdmin(admin.ModelAdmin):
    fields = ['name', 'NID', 'mobile', ('image', 'image_tag'), 'active', ]
    list_display = ['name', 'NID', 'mobile', 'active', ]
    model = NaturalPerson
    list_filter = ['active']
    search_fields = ['name', 'NID']
    readonly_fields = ['image_tag']

    def save_model(self, request, obj, form, change):
        try:
            super(NaturalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(LegalPerson)
class LegalPersonAdmin(admin.ModelAdmin):
    fields = ['name', 'active', ('person_role', 'person_roles')]
    list_display = ['name', 'person_roles', 'active']
    model = LegalPerson
    list_filter = ['active']
    search_fields = ['name', 'person_role']
    readonly_fields = ['person_roles']

    def save_model(self, request, obj, form, change):
        try:
            super(LegalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)
