import os
from functools import reduce
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from ShenasaSolution import settings
from django.utils.html import mark_safe
from Shenasa.utils import to_jalali_full
from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


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


class Bias(models.TextChoices):
    MOST_RIGHT = 2, _('Most Right')
    RIGHT = 1, _('Partly Right')
    NEUTRAL = 0, _('Neutral')
    LEFT = -1, _('Partly Left')
    MOST_LEFT = -2, _('Most Left')


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
    bias = models.CharField(verbose_name=_('Bias'), max_length=10, choices=Bias.choices, default=Bias.NEUTRAL)

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

    def bias_tag(self):
        return mark_safe('<div id="news_bias" class="bias bias%s" alt="%s" title="%s"></div>' %
                         (self.bias, Bias(self.bias).label, Bias(self.bias).label))

    bias_tag.short_description = _('Bias')


class NaturalPerson(Person):
    NID = models.CharField(verbose_name=_('National ID'), max_length=10, unique=True, null=True, blank=True)
    mobile_regex = RegexValidator(
        regex=r'^\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobile = models.CharField(verbose_name=_('Mobile'), validators=[mobile_regex], max_length=17, blank=True)
    image = ResizedImageField(size=[settings.MAX_MEDIUM_IMAGE_WIDTH, settings.MAX_MEDIUM_IMAGE_HEIGHT],
                              verbose_name=_('Person Image'), upload_to='media/', blank=True, null=True)
    news = models.ManyToManyField(News, verbose_name=_('News'), related_name='natural_person_news')

    def image_tag(self):
        if self.image:
            return mark_safe(
                '<a href="%s%s" target="_blank"><img src="%s%s" title="%s" alt="%s" style="max-width:%spx;max-height:%spx;"/></a>' % (
                    settings.MEDIA_URL, self.image, settings.MEDIA_URL, self.image, self.name, self.name,
                    settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT))
        else:
            return mark_safe('<img src="%simg/person-icon.jpg" width="150" height="150" title="%s" alt="%s"/>' % (
                settings.STATIC_URL, self.name, self.name))

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

    def bias_tag(self):
        news_count = self.news.all().count()
        if news_count == 0:
            bias = 0
        else:
            bias = round(reduce(lambda bias, news: bias + int(news.bias), self.news.all(), 0) / news_count)

        def get_bias_label(_bias):
            for b in Bias:
                if int(b.value) == _bias:
                    return b.label

        label = get_bias_label(bias)
        return mark_safe('<div id="person_bias" class="bias bias%s" alt="%s" title="%s"></div>' %
                         (bias, label, label))

    bias_tag.short_description = _('Bias')


@receiver(models.signals.post_delete, sender=NaturalPerson)
def auto_delete_natural_person_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `NaturalPerson` object is deleted.
    """
    if instance.image.name:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        except Exception as e:
            print('Delete error: %s' % e.args[0])


@receiver(models.signals.pre_save, sender=NaturalPerson)
def auto_delete_natural_person_file_on_change(sender, instance, **kwargs):
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

    if not old_image.name:
        return False

    new_image = instance.image

    try:
        if not old_image == new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
    except Exception as e:
        print('Delete error: %s' % e.args[0])
        return False


class PersonRole(models.Model):
    person = models.ForeignKey(NaturalPerson, verbose_name=_('Person'), blank=True, null=True, on_delete=models.CASCADE)
    role = models.CharField(verbose_name=_('Role'), max_length=10, choices=Role.choices, default=Role.STACKHOLDER)
    number_of_shares = models.IntegerField(verbose_name=_('Number of Shares'), default=0)
    amount_of_investment = models.IntegerField(verbose_name=_('Amount of Investment (M rls)'), default=0)

    class Meta:
        unique_together = ['person', 'role']
        verbose_name = _('Person Role')
        verbose_name_plural = _('Person Roles')
        ordering = ['person', 'role']

    def __str__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)

    def __unicode__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)


class LegalPersonQuerySet(models.query.QuerySet):
    def get(self, **kwargs):
        return LegalPerson.objects.all().exclude(id__in=Brand.objects.all().values('pk'))


class CustomManager(models.Manager):
    def get_queryset(self):
        if self.model._meta.label == 'Shenasa.Brand':
            return super().get_queryset()
        else:
            return super().get_queryset().exclude(id__in=Brand.objects.all().values('pk'))


class LegalPersonBase(Person):
    person_role = models.ManyToManyField(PersonRole, verbose_name=_('Natural Key Person'), related_name='%(class)s_person_role')
    legal_role = models.ManyToManyField('LegalRole', verbose_name=_('Legal Key Person'), related_name='%(class)s_legal_role')
    news = models.ManyToManyField(News, verbose_name=_('News'), related_name='%(class)s_news')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def generate_comment(self, pr):
        if pr.role == 'ST':
            return '%s = %s' % (_('Number of Shares'), pr.number_of_shares)
        if pr.role in ('IN', 'IF', 'IV', 'IA'):
            return '%s = %s' % (_('Amount of Investment (M rls)'), pr.amount_of_investment)

    def person_roles_tabular(self):
        return mark_safe(
            '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' %
            (_('Name'), _('Role'), _('Comment'), ''.join(
                '<tr class="row{}"><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(index % 2 + 1, index + 1,
                                                                                             pr.person.name,
                                                                                             Role(pr.role).label,
                                                                                             self.generate_comment(
                                                                                                 pr))
                for
                index, pr in enumerate(self.person_role.all())))
        )

    person_roles_tabular.short_description = _('Selected Natural Key Persons')

    def legal_roles_tabular(self):
        return mark_safe(
            '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' %
            (_('Name'), _('Role'), _('Comment'), ''.join(
                '<tr class="row{}"><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(index % 2 + 1, index + 1,
                                                                                             lr.person.name,
                                                                                             Role(lr.role).label,
                                                                                             self.generate_comment(
                                                                                                 lr))
                for
                index, lr in enumerate(self.legal_role.all())))
        )

    legal_roles_tabular.short_description = _('Selected Legal Key Persons')

    def person_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(pr.role).label, pr.person.name) for index, pr in enumerate(self.person_role.all()))

    person_roles.short_description = _('Selected Natural Key Persons')

    def legal_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(pr.role).label, pr.person.name) for index, pr in enumerate(self.legal_role.all()))

    legal_roles.short_description = _('Selected Legal Key Persons')

    def news_tabular(self):
        return mark_safe(
            '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' %
            (_('Creation Date'), _('Description'), _('Link'), ''.join(
                '<tr class="row{}"><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                    index % 2 + 1, index + 1, to_jalali_full(n.date), n.description, n.link)
                for index, n in enumerate(self.news.all())))
        )

    news_tabular.short_description = _('News')

    @property
    def total_news(self):
        n = reduce(lambda N, n: N | n.person.total_news.all(), self.legal_role.all(),
                   reduce(lambda N, n: N | n.person.news.all(), self.person_role.all(),
                          self.news.all()).distinct()).distinct()
        return n

    def bias_tag(self):
        news = self.total_news
        news_count = news.count()
        if news_count == 0:
            bias = 0
        else:
            bias = round(reduce(lambda bias, news: bias + int(news.bias), news.all(), 0) / news_count)

        def get_bias_label(_bias):
            for b in Bias:
                if int(b.value) == _bias:
                    return b.label

        label = get_bias_label(bias)
        return mark_safe('<div id="person_bias" class="bias bias%s" alt="%s" title="%s"></div>' %
                         (bias, label, label))

    bias_tag.short_description = _('Bias')


class LegalPerson(LegalPersonBase):
    class Meta:
        verbose_name = _('Legal Person')
        verbose_name_plural = _('Legal Persons')

    def __str__(self):
        return '%s: %s' % (_('Legal Person'), self.name)

    def __unicode__(self):
        return '%s: %s' % (_('Legal Person'), self.name)


class LegalRole(models.Model):
    person = models.ForeignKey(LegalPerson, verbose_name=_('Legal Person'), blank=True, null=True,
                               on_delete=models.CASCADE)
    role = models.CharField(verbose_name=_('Role'), max_length=10, choices=Role.choices, default=Role.STACKHOLDER)
    number_of_shares = models.IntegerField(verbose_name=_('Number of Shares'), default=0)
    amount_of_investment = models.IntegerField(verbose_name=_('Amount of Investment (M rls)'), default=0)

    class Meta:
        unique_together = ['person', 'role']
        verbose_name = _('Legal Role')
        verbose_name_plural = _('Legal Roles')
        ordering = ['person', 'role']

    def __str__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)

    def __unicode__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)


class Brand(LegalPersonBase):
    logo = ResizedImageField(size=[settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT],
                             verbose_name=_('Logo'), upload_to='media/', blank=True, null=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return '%s: %s' % (_('Brand'), self.name)

    def __unicode__(self):
        return '%s: %s' % (_('Brand'), self.name)

    def logo_tag(self):
        if self.logo:
            return mark_safe('<a href="%s%s" target="_blank"><img src="%s%s" title="%s" alt="%s"/></a>' % (
                settings.MEDIA_URL, self.logo, settings.MEDIA_URL, self.logo, self.name, self.name))
        else:
            return mark_safe('<img src="%simg/person-icon.jpg" width="150" height="150" title="%s" alt="%s"/>' % (
                settings.STATIC_URL, self.name, self.name))

    logo_tag.short_description = _('Image')


@receiver(models.signals.post_delete, sender=Brand)
def auto_delete_brand_logo_on_delete(sender, instance, **kwargs):
    """
    Deletes logo from filesystem
    when corresponding `Brand` object is deleted.
    """
    if instance.logo.name:
        try:
            if os.path.isfile(instance.logo.path):
                os.remove(instance.logo.path)
        except Exception as e:
            print('Delete error: %s' % e.args[0])


@receiver(models.signals.pre_save, sender=Brand)
def auto_delete_brand_logo_on_change(sender, instance, **kwargs):
    """
    Deletes old logo from filesystem
    when corresponding `Brand` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_logo = Brand.objects.get(pk=instance.pk).logo
    except Brand.DoesNotExist:
        return False

    if not old_logo.name:
        return False

    new_logo = instance.logo
    try:
        if not old_logo == new_logo:
            if os.path.isfile(old_logo.path):
                os.remove(old_logo.path)
    except Exception as e:
        print('Delete error: %s' % e.args[0])
        return False
