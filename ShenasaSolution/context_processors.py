from django.conf import settings


def admin_tel(request):
    return {'ADMIN_TEL': settings.ADMIN_TEL}


def admin_email(request):
    return {'ADMIN_EMAIL': settings.ADMIN_EMAIL}