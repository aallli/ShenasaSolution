from django.contrib import admin
from django.contrib import messages
from Shenasa.models import LegalPerson, NaturalPerson, Role, PersonRole


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
