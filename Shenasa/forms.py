from django import forms


class LegalPersonPersonRoleForm(forms.ModelForm):

    class Media:
        css = {'all': ('css/person_role_admin.css',)}
        js = ('js/custom_admin.js', 'js/legal_person_person_role_admin.js')


class BrandPersonRoleForm(forms.ModelForm):

    class Media:
        css = {'all': ('css/person_role_admin.css',)}
        js = ('js/custom_admin.js', 'js/brand_person_role_admin.js')
