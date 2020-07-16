from django import template
from ShenasaSolution import settings, utlis
from ShenasaSolution.utlis import get_operator

register = template.Library()


@register.simple_tag()
def version():
    return settings.VERSION


@register.simple_tag()
def admin_tel():
    return settings.ADMIN_TEL


@register.simple_tag()
def admin_email():
    return settings.ADMIN_EMAIL


@register.simple_tag()
def chat_server_url():
    return settings.CHAT_SERVER_URL


@register.simple_tag()
def chat_server_token():
    return settings.CHAT_SERVER_TOKEN


@register.simple_tag()
def online_support(request):
    return utlis.online_support()


@register.simple_tag()
def is_online_support_operator(request):
    session = request.session
    if request.user.groups.filter(name=settings.CHAT_SUPPORT_GROUP).count() == 0:
        if 'operator' in session: del session['operator']
        return False
    if 'operator' not in session: get_operator(request, True)
    return session['operator'] is not None


@register.simple_tag()
def on_call(request):
    session = request.session
    if 'operator' not in session: get_operator(request)
    return 'operator' in session and session['operator'] and session['operator']['status'] != 'off'
