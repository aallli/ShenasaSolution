import os
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from ShenasaSolution import settings
from django.utils.html import mark_safe
from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from Shenasa.utils import to_jalali_full

class Role(models.TextChoices):
    FOUNDER = 'FN', _('Founder')
    CHAIRMAN = 'CH', _('Chairman')
    INVESTOR = 'IN', _('Investor')
    INVESTOR_FOREIGN = 'IF', _('Foreign Investor')
    INVESTOR_VC = 'IV', _('Venture Capital')
    INVESTOR_ANGEL = 'IA', _('Angel Investor')
    STACKHOLDER = 'ST', _('Stackholder')
    ACCELERATOR = 'AC', _('Accelerator')
    OWNER = 'OW', _('Owner')
    CMO = 'CM', _('Chief Marketing Officer')
    CCO = 'CC', _('Chief Communication Officer')
    CEO = 'CE', _('Chief Executive Officer')
    CTO = 'CT', _('Chief Technical Officer')
    CO_FOUNDER = 'CF', _('Co Founder')


class Person(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        abstract = True
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class News(models.Model):
    description = models.TextField(verbose_name=_('Description'), max_length=1000, blank=True, null=True)
    link = models.TextField(verbose_name=_('Link'), max_length=200, blank=True, null=True)
    date = models.DateTimeField(verbose_name=_('Creation Date'), null=True, blank=True)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ['-date']

    def __str__(self):
        return '%s : %s' % (to_jalali_full(self.date), self.description[:50])

    def __unicode__(self):
        return '%s : %s' % (to_jalali_full(self.date), self.description[:50])

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        super(News, self).save(*args, **kwargs)

    def title(self):
        return mark_safe(self.description)
    title.short_description = _('Description')


class NaturalPerson(Person):
    NID = models.CharField(verbose_name=_('National ID'), max_length=10, unique=True, null=True, blank=True)
    mobile_regex = RegexValidator(
        regex=r'^\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobile = models.CharField(verbose_name=_('Mobile'), validators=[mobile_regex], max_length=17, blank=True)
    image = ResizedImageField(size=[settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT],
                              verbose_name=_('Person Image'), upload_to='media/', blank=True, null=True)
    news = models.ManyToManyField(News, verbose_name=_('News'), related_name='natural_person_news')

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s%s"/>' % (settings.MEDIA_URL, self.image))
        else:
            return mark_safe('<img src="%simg/person-icon.jpg" width="150" height="150" />' % (settings.STATIC_URL))

    image_tag.short_description = _('Image')

    class Meta:
        verbose_name = _('Natural Person')
        verbose_name_plural = _('Natural Persons')
        ordering = ['name']

    def __str__(self):
        if self.NID:
            return '%s (%s)' % (self.name, self.NID)
        else:
            return self.name

    def __unicode__(self):
        if self.NID:
            return '%s (%s)' % (self.name, self.NID)
        else:
            return self.name

    def news_tabular(self):
        return mark_safe(
            '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' %
            (_('Creation Date'), _('Description'), _('Link'), ''.join(
                '<tr class="row{}"><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                    index % 2 + 1, index + 1, to_jalali_full(n.date), n.description, n.link)
                for index, n in enumerate(self.news.all())))
            )

    news_tabular.short_description = _('News')


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
    role = models.CharField(verbose_name=_('Role'), max_length=10, choices=Role.choices, default=Role.STACKHOLDER)

    class Meta:
        unique_together = ['person', 'role']
        verbose_name = _('Person Role')
        verbose_name_plural = _('Person Roles')
        ordering = ['person', 'role']

    def __str__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)

    def __unicode__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)


class LegalPerson(Person):
    person_role = models.ManyToManyField(PersonRole, verbose_name=_('Key Person'), related_name='person_role')
    news = models.ManyToManyField(News, verbose_name=_('News'), related_name='legal_person_news')

    class Meta:
        verbose_name = _('Legal Person')
        verbose_name_plural = _('Legal Persons')
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def person_roles_tabular(self):
        return mark_safe('<table><thead><tr><th>#</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' %
                         (_('Name'), _('Role'), ''.join(
                             '<tr class="row{}"><td>{}</td><td>{}</td><td>{}</td></tr>'.format(index % 2 + 1, index + 1,
                                                                                               pr.person.name,
                                                                                               Role(pr.role).label) for
                             index, pr in enumerate(self.person_role.all())))
                         )

    person_roles_tabular.short_description = _('Selected Legal Persons')

    def person_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(pr.role).label, pr.person.name) for index, pr in enumerate(self.person_role.all()))

    person_roles.short_description = _('Selected Legal Persons')

    def news_tabular(self):
        return mark_safe(
            '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' %
            (_('Creation Date'), _('Description'), _('Link'), ''.join(
                '<tr class="row{}"><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                    index % 2 + 1, index + 1, to_jalali_full(n.date), n.description, n.link)
                for index, n in enumerate(self.news.all())))
            )

    news_tabular.short_description = _('News')
