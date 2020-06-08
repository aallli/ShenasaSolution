from django import forms

class PersonRoleForm(forms.ModelForm):

    class Media:
        css = {'all': ('css/person_role_admin.css',)}
        js = ('js/person_role_admin.js',)