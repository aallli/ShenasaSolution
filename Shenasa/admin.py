from django.db import models
from django.contrib import admin
from django.conf import settings
from django.forms import TextInput
from django.contrib import messages
from Shenasa.utils import to_jalali_full
from django.db.transaction import atomic
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from Shenasa.forms import LegalPersonPersonRoleForm, BrandPersonRoleForm
from Shenasa.models import LegalPerson, NaturalPerson, News, LegalRole, Brand, LegalPersonPersonRole, \
    BrandPersonRole


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE


class NaturalPersonNewsInline(admin.TabularInline):
    model = NaturalPerson.news.through
    verbose_name = _("Natural Person News")
    verbose_name_plural = _("Natural Person News")


class LegalPersonPersonRoleInline(admin.TabularInline):
    model = LegalPersonPersonRole
    form = LegalPersonPersonRoleForm
    fields = ['person', 'role', 'number_of_stocks', 'amount_of_investment']
    verbose_name = _("Person Role")
    verbose_name_plural = _("Person Roles")


class LegalPersonLegalRoleInline(admin.TabularInline):
    model = LegalPerson.legal_role.through
    verbose_name = _("Legal Role")
    verbose_name_plural = _("Legal Roles")


class LegalPersonNewsInline(admin.TabularInline):
    model = LegalPerson.news.through
    verbose_name = _("Legal Person News")
    verbose_name_plural = _("Legal Person News")


class BrandPersonRoleInline(admin.TabularInline):
    model = BrandPersonRole
    form = BrandPersonRoleForm
    fields = ['person', 'role', 'number_of_stocks', 'amount_of_investment']
    verbose_name = _("Person Role")
    verbose_name_plural = _("Person Roles")


class BrandRoleInline(admin.TabularInline):
    model = Brand.legal_role.through
    verbose_name = _("Legal Role")
    verbose_name_plural = _("Legal Roles")


class BrandNewsInline(admin.TabularInline):
    model = Brand.news.through
    verbose_name = _("Brand News")
    verbose_name_plural = _("Brand News")


@admin.register(LegalRole)
class LegalRoleAdmin(BaseModelAdmin):
    fields = [('person', 'role', 'number_of_stocks', 'amount_of_investment'), ]
    list_display = ['person', 'role', ]
    list_display_links = ['person', 'role', ]
    model = LegalRole
    search_fields = ['person__name']
    list_filter = ['person', 'role']
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size': '20'})},
    }

    def save_model(self, request, obj, form, change):
        try:
            super(LegalRoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(News)
class NewsAdmin(ModelAdminJalaliMixin, SummernoteModelAdmin, BaseModelAdmin):
    summernote_fields = ('description',)
    fields = [('date', 'bias', 'bias_tag',), 'description', 'link', ]
    list_display = ['bias_tag', 'title', 'get_created_jalali']
    list_display_links = ['title', 'get_created_jalali']
    search_fields = ['description', 'link']
    readonly_fields = ['bias_tag']
    model = News
    inlines = [
        NaturalPersonNewsInline,
        LegalPersonNewsInline,
        BrandNewsInline,
    ]
    list_filter = ['date']
    save_on_top = True

    class Media:
        js = ('js/custom_admin.js', 'js/news_admin.js')

    def save_model(self, request, obj, form, change):
        try:
            super(NewsAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)

    def get_created_jalali(self, obj):
        return to_jalali_full(obj.date)

    get_created_jalali.short_description = _('Creation Date')
    get_created_jalali.admin_order_field = 'date'


@admin.register(NaturalPerson)
class NaturalPersonAdmin(BaseModelAdmin):
    list_display = ['bias_tag', 'name', 'NID', 'mobile', 'total_investment_string_formatted',
                    'total_purchased_stocks_string_formatted', 'active', ]
    list_display_links = ['name', 'NID', 'mobile', 'total_investment_string_formatted',
                          'total_purchased_stocks_string_formatted', 'active', ]
    model = NaturalPerson
    list_filter = ['active']
    search_fields = ['name', 'NID', 'mobile']
    readonly_fields = ['image_tag', 'total_investment_tabular', 'total_purchased_stocks_tabular', 'news_tabular',
                       'total_investment_string_formatted', 'total_purchased_stocks_string_formatted',
                       'bias_tag']
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(NaturalPersonAdmin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            NaturalPersonNewsInline,
        ]
        permissions = request.user.get_all_permissions()
        if request.user.is_superuser:
            self.fields = [('name', 'bias_tag'), 'NID', 'mobile', 'active', ('image', 'image_tag'),
                           ('total_investment_string_formatted', 'total_investment_tabular'),
                           ('total_purchased_stocks_string_formatted', 'total_purchased_stocks_tabular'),
                           'news_tabular']
        elif 'Shenasa.add_naturalperson' in permissions or 'Shenasa.change_naturalperson' in permissions or 'Shenasa.delete_naturalperson' in permissions:
            self.fields = [('name', 'bias_tag'), 'NID',
                           ('mobile', 'total_investment_string_formatted', 'total_purchased_stocks_string_formatted'),
                           'active', ('image', 'image_tag')]
        else:
            self.inlines = []
            self.fields = [('name', 'bias_tag'), 'NID', 'mobile', 'active', ('image', 'image_tag'),
                           ('total_investment_string_formatted', 'total_investment_tabular'),
                           ('total_purchased_stocks_string_formatted', 'total_purchased_stocks_tabular'),
                           'news_tabular']

        return form

    def save_model(self, request, obj, form, change):
        try:
            super(NaturalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(LegalPerson)
class LegalPersonAdmin(BaseModelAdmin):
    list_display = ['bias_tag', 'name', 'person_roles', 'legal_roles',
                    'total_investment_string_formatted', 'total_purchased_stocks_string_formatted',
                    'total_fund_string_formatted', 'total_sold_stocks_string_formatted',
                    'active']
    list_display_links = ['name', 'person_roles', 'legal_roles',
                          'total_investment_string_formatted', 'total_purchased_stocks_string_formatted',
                          'total_fund_string_formatted', 'total_sold_stocks_string_formatted',
                          'active']
    model = LegalPerson
    list_filter = ['active', 'person_role__person', 'person_role__role']
    search_fields = ['name', 'person_role__person__name']
    readonly_fields = ['person_roles', 'person_roles_tabular', 'legal_roles_tabular', 'total_investment_tabular',
                       'total_investment_string_formatted', 'total_purchased_stocks_string_formatted',
                       'total_purchased_stocks_tabular', 'news_tabular',
                       'total_fund_string_formatted', 'total_sold_stocks_string_formatted',
                       'total_fund_tabular', 'total_sold_stocks_tabular',
                       'bias_tag']
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(LegalPersonAdmin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            LegalPersonPersonRoleInline,
            LegalPersonLegalRoleInline,
            LegalPersonNewsInline,
        ]
        permissions = request.user.get_all_permissions()
        if request.user.is_superuser:
            self.fields = [('name', 'active', 'bias_tag'),
                           ('person_roles_tabular', 'legal_roles_tabular'),
                           ('total_investment_string_formatted', 'total_investment_tabular'),
                           ('total_purchased_stocks_string_formatted', 'total_purchased_stocks_tabular'),
                           ('total_fund_string_formatted', 'total_fund_tabular'),
                           ('total_sold_stocks_string_formatted', 'total_sold_stocks_tabular'),
                           'news_tabular']
        elif 'Shenasa.add_legalperson' in permissions or 'Shenasa.change_legalperson' in permissions or 'Shenasa.delete_legalperson' in permissions:
            self.fields = [('name', 'active', 'bias_tag'),
                           ('total_investment_string_formatted', 'total_purchased_stocks_string_formatted'),
                           ('total_fund_string_formatted', 'total_sold_stocks_string_formatted'),
                           ]
        else:
            self.inlines = []
            self.fields = [('name', 'active', 'bias_tag'),
                           ('person_roles_tabular', 'legal_roles_tabular'),
                           ('total_investment_string_formatted', 'total_investment_tabular'),
                           ('total_purchased_stocks_string_formatted', 'total_purchased_stocks_tabular'),
                           ('total_fund_string_formatted', 'total_fund_tabular'),
                           ('total_sold_stocks_string_formatted', 'total_sold_stocks_tabular'),
                           'news_tabular']
        return form

    def save_model(self, request, obj, form, change):
        try:
            super(LegalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)

    @atomic()
    def save_formset(self, request, form, formset, change):
        try:
            instances = formset.save(commit=False)
            if formset.prefix == 'LegalPerson_legal_role':
                for lp in formset.cleaned_data:
                    if 'id' in lp and not lp['id'] and lp['legalrole'].person.pk == formset.instance.pk:
                        raise Exception(_('Self relation from "%(legalrole)s" to "%(legalrole)s" is not valid.') % {
                            'legalrole': formset.instance.name})
            formset.save_m2m()
            super(LegalPersonAdmin, self).save_formset(request, form, formset, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(Brand)
class BrandAdmin(BaseModelAdmin):
    list_display = ['bias_tag', 'name', 'person_roles', 'legal_roles',
                    'total_fund_string_formatted', 'total_sold_stocks_string_formatted',
                    'active']
    list_display_links = ['name', 'person_roles', 'legal_roles',
                          'total_fund_string_formatted', 'total_sold_stocks_string_formatted',
                          'active']
    model = Brand
    list_filter = ['active', ('person_role__person', custom_titled_filter(_('Person Role'))),
                   ('legal_role__person', custom_titled_filter(_('Legal Role')))]
    search_fields = ['name', 'person_role__person__name']
    readonly_fields = ['person_roles', 'person_roles_tabular', 'legal_roles_tabular', 'news_tabular',
                       'total_fund_string_formatted', 'total_sold_stocks_string_formatted',
                       'total_fund_tabular', 'total_sold_stocks_tabular',
                       'logo_tag', 'bias_tag']
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(BrandAdmin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            BrandPersonRoleInline,
            BrandRoleInline,
            BrandNewsInline,
        ]
        permissions = request.user.get_all_permissions()
        if request.user.is_superuser:
            self.fields = [('name', 'active', 'bias_tag'), ('logo', 'logo_tag'),
                           ('person_roles_tabular', 'legal_roles_tabular'),
                           ('total_fund_string_formatted', 'total_fund_tabular'),
                           ('total_sold_stocks_string_formatted', 'total_sold_stocks_tabular'),
                           'news_tabular']
        elif 'Shenasa.add_brand' in permissions or 'Shenasa.change_brand' in permissions or 'Shenasa.delete_brand' in permissions:
            self.fields = [('name', 'active', 'bias_tag'), ('logo', 'logo_tag'),
                           ('total_fund_string_formatted', 'total_sold_stocks_string_formatted'),
                           ]
        else:
            self.inlines = []
            self.fields = [('name', 'active', 'bias_tag'), ('logo', 'logo_tag'),
                           ('person_roles_tabular', 'legal_roles_tabular'),
                           ('total_fund_string_formatted', 'total_fund_tabular'),
                           ('total_sold_stocks_string_formatted', 'total_sold_stocks_tabular'),
                           'news_tabular']

        return form

    def save_model(self, request, obj, form, change):
        try:
            super(BrandAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)
