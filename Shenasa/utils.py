from jalali_date import datetime2jalali
from django.utils.translation import ugettext_lazy as _


def to_jalali_full(date):
    return datetime2jalali(date).strftime('%H:%M:%S %y/%m/%d')


msgid = _("welcome")
msgid = _("Admin Interface")
msgid = _("Django Summernote")
msgid = _("Naturalperson")
msgid = _("Legalperson")
msgid = _("Theme")
msgid = _("Themes")
msgid = _("Attachment")
msgid = _("Attachments")
