from django.contrib import admin
from django.contrib import messages
from jalali_date import datetime2jalali
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from Shenasa.models import LegalPerson, NaturalPerson, PersonRole, News
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


class LegalPersonInline(admin.TabularInline):
    model = LegalPerson.person_role.through
    verbose_name = _("Person Role")
    verbose_name_plural = _("Person Roles")


@admin.register(PersonRole)
class PersonRoleAdmin(admin.ModelAdmin):
    fields = [('person', 'role'), ]
    list_display = ['person', 'role', ]
    model = PersonRole
    search_fields = ['person__name']
    list_filter = ['role']
    inlines = [
        LegalPersonInline,
    ]

    def save_model(self, request, obj, form, change):
        try:
            super(PersonRoleAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


@admin.register(News)
class NewsAdmin(ModelAdminJalaliMixin, SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ['title', 'get_created_jalali']
    search_fields = ['description', 'link']
    model = News

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
    fields = [('name', 'active'), 'person_roles_tabular']
    list_display = ['name', 'person_roles', 'active']
    model = LegalPerson
    list_filter = ['active', 'person_role__role']
    search_fields = ['name', 'person_role__person__name']
    readonly_fields = ['person_roles', 'person_roles_tabular']
    inlines = [
        LegalPersonInline,
    ]
    exclude = ('person_role',)

    def save_model(self, request, obj, form, change):
        try:
            super(LegalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)
