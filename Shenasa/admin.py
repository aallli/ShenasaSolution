from django.contrib import admin
from django.contrib import messages
from Shenasa.models import Person, LegalPerson, NaturalPerson


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
    fields = ['name', 'active', 'CEO']
    list_display = ['name', 'CEO', 'active', ]
    model = LegalPerson
    list_filter = ['active']
    search_fields = ['name', 'CEO']

    def save_model(self, request, obj, form, change):
        try:
            super(LegalPersonAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)