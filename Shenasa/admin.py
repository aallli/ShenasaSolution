from django.contrib import admin
from django.contrib import messages
from Shenasa.utils import to_jalali_full
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from Shenasa.models import LegalPerson, NaturalPerson, PersonRole, News, LegalRole
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


class PersonRoleInline(admin.TabularInline):
    model = LegalPerson.person_role.through
    verbose_name = _("Person Role")
    verbose_name_plural = _("Person Roles")


class LegalRoleInline(admin.TabularInline):
    model = LegalPerson.legal_role.through
    verbose_name = _("Legal Role")
    verbose_name_plural = _("Legal Roles")


class LegalPersonNewsInline(admin.TabularInline):
    model = LegalPerson.news.through
    verbose_name = _("Legal Person News")
    verbose_name_plural = _("Legal Person News")


class NaturalPersonNewsInline(admin.TabularInline):
    model = NaturalPerson.news.through
    verbose_name = _("Natural Person News")
    verbose_name_plural = _("Natural Person News")


@admin.register(PersonRole)
class PersonRoleAdmin(admin.ModelAdmin):
    fields = [('person', 'role'), ]
    list_display = ['person', 'role', ]
    model = PersonRole
    search_fields = ['person__name']
    list_filter = ['role']

    def save_model(self, request, obj, form, change):
        try:
            super(PersonRoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(LegalRole)
class LegalRoleAdmin(admin.ModelAdmin):
    fields = [('person', 'role'), ]
    list_display = ['person', 'role', ]
    model = LegalRole
    search_fields = ['person__name']
    list_filter = ['role']

    def save_model(self, request, obj, form, change):
        try:
            super(LegalRoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(News)
class NewsAdmin(ModelAdminJalaliMixin, SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ['title', 'get_created_jalali']
    search_fields = ['description', 'link']
    model = News
    inlines = [
        NaturalPersonNewsInline,
        LegalPersonNewsInline,
    ]

    class Media:
        css = {'all': ('css/custom_admin.css',)}
        js = ('js/custom_admin.js',)

    #
    # def get_form(self, request, obj=None, **kwargs):
    #     self.fields = ['description', 'link', 'date', ]
    #     form = super(NewsAdmin, self).get_form(request, obj, **kwargs)
    #     if obj.description == '<p>cccccccccccccccccccccccccccccc</p>':
    #         self.fields.remove("link")
    #
    #     return form

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
class NaturalPersonAdmin(admin.ModelAdmin):
    fields = ['name', 'NID', 'mobile', 'active', ('image', 'image_tag'), 'news_tabular']
    list_display = ['name', 'NID', 'mobile', 'active', ]
    model = NaturalPerson
    list_filter = ['active']
    search_fields = ['name', 'NID']
    readonly_fields = ['image_tag', 'news_tabular']

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
class LegalPersonAdmin(admin.ModelAdmin):
    fields = [('name', 'active'), ('person_roles_tabular', 'legal_roles_tabular'), 'news_tabular']
    list_display = ['name', 'person_roles', 'legal_roles', 'active']
    model = LegalPerson
    list_filter = ['active', 'person_role__role']
    search_fields = ['name', 'person_role__person__name']
    readonly_fields = ['person_roles', 'person_roles_tabular', 'legal_roles_tabular', 'news_tabular']

    def get_form(self, request, obj=None, **kwargs):
        form = super(LegalPersonAdmin, self).get_form(request, obj=obj, **kwargs)
        self.inlines = [
            PersonRoleInline,
            LegalRoleInline,
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
