from django.apps import apps
from django import template
from django.contrib.admin import site
from django.utils.text import capfirst
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.inclusion_tag('admin/reordered_app_list.html', takes_context=True)
def render_model_list(context):
    model_dict = {}
    app_dict = {}
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = User.has_module_perms(User, app_label)
        info = (app_label, model._meta.model_name)
        if has_module_perms:
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
            }
        try:
            model_dict['admin_url'] = reverse(
                'admin:%s_%s_changelist' % info,
                current_app=site.name
            )
        except NoReverseMatch:
            pass
        try:
            model_dict['add_url'] = reverse(
                'admin:%s_%s_add' % info,
                current_app=site.name
            )
        except NoReverseMatch:
            pass
        if app_label in app_dict:
            app_dict[app_label]['models'].append(model_dict)
        else:
            app_dict[app_label] = {
                'name': apps.get_app_config(app_label).verbose_name,
                'app_label': app_label,
                'app_url': reverse(
                    'admin:app_list',
                    kwargs={'app_label': app_label},
                    current_app=site.name
                ),
                'has_module_perms': has_module_perms,
                'models': [model_dict],
            }
    app_ordering = {
        'Shenasa': 1,
        'شناسا': 1,
        'Admin Interface': 3,
        'رابط کاربری': 3,
        'Django Summernote': 4,
        'ادیتور پیشرفته متن': 4,
        'Authentication and Authorization': 2,
        'بررسی اصالت و اجازه\u200cها': 2,
    }

    model_ordering = {
        'Themes': 1,
        'شمایل گرافیکی': 1,
        'Groups': 2,
        'گروه\u200cها': 2,
        'Users': 3,
        'کاربرها': 3,
        'Attachments': 4,
        'ضمایم': 4,
        'Brands': 5,
        'نمانام های رسانه ای': 5,
        'Natural Persons': 6,
        'اشخاص حقیقی': 6,
        'Legal Persons': 7,
        'اشخاص حقوقی': 7,
        'News': 9,
        'اخبار': 9,
        'Person Roles': 10,
        'سمتهای حقیقی': 10,
        'Legal Roles': 11,
        'سمتهای حقوقی': 11,
    }

    app_list = sorted(app_dict.values(), key=lambda x: app_ordering[x['name']])
    # Sort the models by model ordering dict within each app.
    for app in app_list: app['models'].sort(key=lambda x: model_ordering[x['name']])

    return {'app_list': app_list, 'request': context['request']}
