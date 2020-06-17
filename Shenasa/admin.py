from django.conf import settings
from django.db import models
from django.contrib import admin
from django.db.transaction import atomic
from django.forms import TextInput
from django.contrib import messages
from Shenasa.utils import to_jalali_full
from Shenasa.forms import PersonRoleForm
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from Shenasa.models import LegalPerson, NaturalPerson, PersonRole, News, LegalRole, Brand1
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE


class LegalPersonPersonRoleInline(admin.TabularInline):
    model = LegalPerson.person_role.through
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
    model = Brand1.person_role.through
    verbose_name = _("Person Role")
    verbose_name_plural = _("Person Roles")


class BrandRoleInline(admin.TabularInline):
    model = Brand1.legal_role.through
    verbose_name = _("Legal Role")
    verbose_name_plural = _("Legal Roles")


class BrandNewsInline(admin.TabularInline):
    model = Brand1.news.through
    verbose_name = _("Brand News")
    verbose_name_plural = _("Brand News")


class NaturalPersonNewsInline(admin.TabularInline):
    model = NaturalPerson.news.through
    verbose_name = _("Natural Person News")
    verbose_name_plural = _("Natural Person News")


@admin.register(Brand1)
class Brand1Admin(BaseModelAdmin):
    fields = [('name', 'active', 'bias_tag'), ('logo', 'logo_tag'), ('person_roles_tabular', 'legal_roles_tabular'), 'news_tabular']
    list_display = ['bias_tag', 'name', 'person_roles', 'legal_roles', 'active']
    list_display_links = ['name', 'person_roles', 'legal_roles', 'active']
    model = Brand1
    list_filter = ['active', ('person_role__person', custom_titled_filter(_('Person Role'))),
                   ('legal_role__person', custom_titled_filter(_('Legal Role')))]
    search_fields = ['name', 'person_role__person__name']
    readonly_fields = ['person_roles_tabular', 'legal_roles_tabular', 'news_tabular', 'logo_tag', 'bias_tag']
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(Brand1Admin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            BrandPersonRoleInline,
            BrandRoleInline,
            BrandNewsInline,
        ]
        permissions = request.user.get_all_permissions()
        if not ('Shenasa.add_legalperson' in permissions or
                        'Shenasa.change_legalperson' in permissions or
                        'Shenasa.delete_legalperson' in permissions):
            self.inlines = []
        return form

    def save_model(self, request, obj, form, change):
        try:
            super(Brand1Admin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(PersonRole)
class PersonRoleAdmin(BaseModelAdmin):
    fields = [('person', 'role', 'number_of_shares', 'amount_of_investment'), ]
    list_display = ['person', 'role']
    list_display_links = ['person', 'role']
    model = PersonRole
    search_fields = ['person__name']
    list_filter = ['person', 'role']
    form = PersonRoleForm
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size': '20'})},
    }

    def save_model(self, request, obj, form, change):
        try:
            super(PersonRoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(LegalRole)
class LegalRoleAdmin(BaseModelAdmin):
    fields = [('person', 'role', 'number_of_shares', 'amount_of_investment'), ]
    list_display = ['person', 'role', ]
    list_display_links = ['person', 'role', ]
    model = LegalRole
    search_fields = ['person__name']
    list_filter = ['person', 'role']
    form = PersonRoleForm
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
    fields = [('date', 'bias', 'bias_tag', ), 'description', 'link', ]
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
    fields = [('name', 'bias_tag'), 'NID', 'mobile', 'active', ('image', 'image_tag'), 'news_tabular']
    list_display = ['bias_tag', 'name', 'NID', 'mobile', 'active', ]
    list_display_links = ['name', 'NID', 'mobile', 'active', ]
    model = NaturalPerson
    list_filter = ['active']
    search_fields = ['name', 'NID', 'mobile']
    readonly_fields = ['image_tag', 'news_tabular', 'bias_tag']
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(NaturalPersonAdmin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            NaturalPersonNewsInline,
        ]
        permissions = request.user.get_all_permissions()
        if not ('Shenasa.add_naturalperson' in permissions or
                        'Shenasa.change_naturalperson' in permissions or
                        'Shenasa.delete_naturalperson' in permissions):
            self.inlines = []
        return form

    def save_model(self, request, obj, form, change):
        try:
            super(NaturalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(LegalPerson)
class LegalPersonAdmin(BaseModelAdmin):
    fields = [('name', 'active', 'bias_tag'), ('person_roles_tabular', 'legal_roles_tabular'), 'news_tabular']
    list_display = ['bias_tag', 'name', 'person_roles', 'legal_roles', 'active']
    list_display_links = ['name', 'person_roles', 'legal_roles', 'active']
    model = LegalPerson
    list_filter = ['active', 'person_role__person', 'person_role__role']
    search_fields = ['name', 'person_role__person__name']
    readonly_fields = ['person_roles', 'person_roles_tabular', 'legal_roles_tabular', 'news_tabular', 'bias_tag']
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(LegalPersonAdmin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            LegalPersonPersonRoleInline,
            LegalPersonLegalRoleInline,
            LegalPersonNewsInline,
        ]
        permissions = request.user.get_all_permissions()
        if not ('Shenasa.add_legalperson' in permissions or
                        'Shenasa.change_legalperson' in permissions or
                        'Shenasa.delete_legalperson' in permissions):
            self.inlines = []
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
