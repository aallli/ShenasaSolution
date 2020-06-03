import os
from django.db import models
from django.dispatch import receiver
from ShenasaSolution import settings
from django.utils.html import mark_safe
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        abstract = True
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class NaturalPerson(Person):
    NID = models.CharField(verbose_name=_('National ID'), max_length=10, unique=True, null=True, blank=True)
    mobile_regex = RegexValidator(
        regex=r'^\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobile = models.CharField(verbose_name=_('Mobile'), validators=[mobile_regex], max_length=17, blank=True)
    image = models.ImageField(verbose_name=_('Person Image'), upload_to='media/', blank=True, null=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s%s" width="150" height="150" />' % (settings.MEDIA_URL, self.image))
        else:
            return mark_safe('<img src="%simg/person-icon.jpg" width="150" height="150" />' % (settings.STATIC_URL))

    image_tag.short_description = _('Image')

    class Meta:
        verbose_name = _("Natural Person")
        verbose_name_plural = _("Natural Persons")
        ordering = ['name']

    def __str__(self):
        return '%s (%s)' % (self.name, self.NID)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.NID)


@receiver(models.signals.post_delete, sender=NaturalPerson)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `NaturalPerson` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=NaturalPerson)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `NaturalPerson` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = NaturalPerson.objects.get(pk=instance.pk).image
    except NaturalPerson.DoesNotExist:
        return False

    new_image = instance.image
    try:
        if not old_image == new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
    except:
        return False


class PersonRole(models.Model):
    person = models.ForeignKey(NaturalPerson, verbose_name=_('Person'), blank=True, null=True, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, verbose_name=_('Role'), blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['person', 'role']
        verbose_name = _("Person Role")
        verbose_name_plural = _("Person Roles")
        ordering = ['person', 'role']

    def __str__(self):
        return '%s (%s)' % (self.person, self.role)

    def __unicode__(self):
        return '%s (%s)' % (self.person, self.role)


class LegalPerson(Person):
    person_role = models.ManyToManyField(PersonRole, verbose_name=_('Key Person'))

    class Meta:
        verbose_name = _("Legal Person")
        verbose_name_plural = _("Legal Persons")
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)

    def __unicode__(self):
        return '%s' % (self.name)

    def person_roles(self):
        return ', '.join('{}: {}'.format(pr.role.name, pr.person.name)  for pr in self.person_role.all())
    person_roles.short_description = _("Selected Legal Persons")
