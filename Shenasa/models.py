import os
import locale
from functools import reduce
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.dispatch import receiver
from ShenasaSolution import settings
from django.utils.html import mark_safe
from Shenasa.utils import to_jalali_full
from django_resized import ResizedImageField
from ShenasaSolution.utlis import get_admin_url
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

locale.setlocale(locale.LC_ALL, '')


def hide_title(class_name):
    return '<script type="text/javascript">document.getElementsByClassName("%s")[0].style.display = "none";</script>' % class_name


class Role(models.TextChoices):
    FOUNDER = 'FN', _('Founder')
    CHAIRMAN = 'CH', _('Chairman')
    VICE_CHAIRMAN = 'VC', _('Vice Chairman')
    MEMBER_BOARD = 'MB', _('Member of the Board')
    INVESTOR = 'IN', _('Investor')
    INVESTOR_FOREIGN = 'IF', _('Foreign Investor')
    INVESTOR_VC = 'IV', _('Venture Capital')
    INVESTOR_ANGEL = 'IA', _('Angel Investor')
    STOCKHOLDER = 'ST', _('Stockholder')
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

    total_investment_title = _('Total of Investment (M rls)')
    total_purchased_stocks_title = _('Total Purchased Stocks')
    total_fund_title = _('Total of Fund (M rls)')
    total_sold_stocks_title = _('Total Sold Stocks')
    roles_tabular_title = _('Total Roles')

    def roles_tabular(self):
        pass

    roles_tabular.short_description = roles_tabular_title

    def total_investment(self):
        pass

    total_investment.short_description = total_investment_title

    def total_investment_string_formatted(self):
        total_investment = self.total_investment()
        if total_investment:
            return '{:n}'.format(total_investment)
        else:
            return 0

    total_investment_string_formatted.short_description = total_investment_title

    def total_investment_tabular(self):
        pass

    total_investment_tabular.short_description = total_investment_title

    def total_purchased_stocks(self):
        pass

    total_purchased_stocks.short_description = total_purchased_stocks_title

    def total_purchased_stocks_string_formatted(self):
        total_purchased_stocks = self.total_purchased_stocks()
        if total_purchased_stocks:
            return '{:n}'.format(total_purchased_stocks)
        else:
            return 0

    total_purchased_stocks_string_formatted.short_description = total_purchased_stocks_title

    def total_purchased_stocks_tabular(self):
        pass

    total_purchased_stocks_tabular.short_description = total_purchased_stocks_title

    def total_fund(self):
        pass

    total_fund.short_description = total_fund_title

    def total_fund_string_formatted(self):
        total_fund = self.total_fund()
        if total_fund:
            return '{:n}'.format(total_fund)
        else:
            return 0

    total_fund_string_formatted.short_description = total_fund_title

    def total_sold_stocks(self):
        pass

    total_sold_stocks.short_description = total_sold_stocks_title

    def total_sold_stocks_string_formatted(self):
        total_sold_stocks = self.total_sold_stocks()
        if total_sold_stocks:
            return '{:n}'.format(total_sold_stocks)
        else:
            return 0

    total_sold_stocks_string_formatted.short_description = total_sold_stocks_title

    def total_fund_tabular(self):
        pass

    def total_sold_stocks_tabular(self):
        pass

    total_sold_stocks_tabular.short_description = total_sold_stocks_title

    def news_tabular(self):
        result = ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(n), to_jalali_full(n.date), get_admin_url(n), n.description,
                get_admin_url(n), n.link)
            for index, n in enumerate(self.news.all()))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Creation Date'), _('Description'), _('Link'), result)
        else:
            result = hide_title('form-row field-news_tabular')

        return mark_safe(result)

    news_tabular.short_description = _('News')


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

    def link_tag(self):
        return mark_safe('<div class="link_tag">%s</div>' % ' - '.join('<a href="%s" target="_blank">%s</a>' % (n, n)  for n in self.link.split(' ')))

    link_tag.short_description = _('Link')


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

    def total_investment(self):
        result = 0
        roles = LegalPersonPersonRole.objects.filter(person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        roles = BrandPersonRole.objects.filter(person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        return result

    def total_purchased_stocks(self):
        result = 0
        roles = LegalPersonPersonRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        roles = BrandPersonRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        return result

    def roles_tabular(self):
        result = ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(lppr.target_person), lppr.target_person.name,
                get_admin_url(lppr.target_person), Role(lppr.role).label,
                get_admin_url(lppr.target_person), lppr.target_person.generate_comment(lppr))
            for index, lppr in enumerate(LegalPersonPersonRole.objects.filter(person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

        result += ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(bpr.target_person), bpr.target_person.name,
                get_admin_url(bpr.target_person), Role(bpr.role).label,
                get_admin_url(bpr.target_person), bpr.target_person.generate_comment(bpr))
            for index, bpr in enumerate(BrandPersonRole.objects.filter(person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    roles_tabular.short_description = Person.roles_tabular.short_description

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

    def total_investment_tabular(self):
        result = ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(lppr.target_person), lppr.target_person.name,
                get_admin_url(lppr.target_person), Role(lppr.role).label,
                get_admin_url(lppr.target_person), lppr.target_person.generate_comment(lppr))
            for index, lppr in enumerate(LegalPersonPersonRole.objects.filter(person=self).filter(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        result += ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(bpr.target_person), bpr.target_person.name,
                get_admin_url(bpr.target_person), Role(bpr.role).label,
                get_admin_url(bpr.target_person), bpr.target_person.generate_comment(bpr))
            for index, bpr in enumerate(BrandPersonRole.objects.filter(person=self).filter(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    def total_purchased_stocks_tabular(self):
        result = ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(lppr.target_person), lppr.target_person.name,
                get_admin_url(lppr.target_person), Role(lppr.role).label,
                get_admin_url(lppr.target_person), lppr.target_person.generate_comment(lppr))
            for index, lppr in
            enumerate(LegalPersonPersonRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)))

        result += ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(bpr.target_person), bpr.target_person.name,
                get_admin_url(bpr.target_person), Role(bpr.role).label,
                get_admin_url(bpr.target_person), bpr.target_person.generate_comment(bpr))
            for index, bpr in
            enumerate(BrandPersonRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)))
        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)


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


class RoleBase(models.Model):
    person = models.SlugField()
    target_person = models.SlugField()
    role = models.CharField(verbose_name=_('Role'), max_length=10, choices=Role.choices, default=Role.STOCKHOLDER)
    number_of_stocks = models.IntegerField(verbose_name=_('Number of Stocks'), default=0)
    amount_of_investment = models.IntegerField(verbose_name=_('Amount of Investment (M rls)'), default=0)

    class Meta:
        unique_together = ['person', 'target_person', 'role']
        verbose_name = _('Person Role')
        verbose_name_plural = _('Person Roles')
        ordering = ['person', 'role', 'target_person']
        abstract = True

    def __str__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)

    def __unicode__(self):
        return '%s (%s)' % (self.person, Role(self.role).label)

    def number_of_stocks_string_formatted(self):
        if self.number_of_stocks:
            return '{:n}'.format(self.number_of_stocks)
        else:
            return 0

    def amount_of_investment_string_formatted(self):
        if self.amount_of_investment:
            return '{:n}'.format(self.amount_of_investment)
        else:
            return 0


class LegalPersonPersonRole(RoleBase):
    person = models.ForeignKey(NaturalPerson, verbose_name=_('Person'), blank=False, null=False,
                               on_delete=models.CASCADE, related_name='legal_person_person_role_person')
    target_person = models.ForeignKey('LegalPerson', verbose_name=_('Legal Person'), blank=False, null=False,
                                      on_delete=models.CASCADE, related_name='legal_person_person_role_target_person')


class BrandPersonRole(RoleBase):
    person = models.ForeignKey(NaturalPerson, verbose_name=_('Person'), blank=False, null=False,
                               on_delete=models.CASCADE, related_name='brand_person_role_person')
    target_person = models.ForeignKey('Brand', verbose_name=_('Brand'), blank=False, null=False,
                                      on_delete=models.CASCADE, related_name='brand_person_role_target_person')


class LegalPersonLegalRole(RoleBase):
    person = models.ForeignKey('LegalPerson', verbose_name=_('Legal Person'), blank=False, null=False,
                               on_delete=models.CASCADE, related_name='legal_person_legal_role_person')
    target_person = models.ForeignKey('LegalPerson', verbose_name=_('Legal Person'), blank=False, null=False,
                                      on_delete=models.CASCADE, related_name='legal_person_legal_role_target_person')


class BrandLegalRole(RoleBase):
    person = models.ForeignKey('LegalPerson', verbose_name=_('Legal Person'), blank=False, null=False,
                               on_delete=models.CASCADE, related_name='brand_legal_role_person')
    target_person = models.ForeignKey('Brand', verbose_name=_('Brand'), blank=False, null=False,
                                      on_delete=models.CASCADE, related_name='brand_legal_role_target_person')


class LegalPersonBase(Person):
    news = models.ManyToManyField(News, verbose_name=_('News'), related_name='%(class)s_news')

    class Meta(Person.Meta):
        abstract = True

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def total_investment(self):
        pass

    def total_purchased_stocks(self):
        pass

    def total_fund(self):
        pass

    def total_sold_stocks(self):
        pass

    def generate_comment(self, pr):
        if pr.role == 'ST':
            return '%s = %s' % (_('Number of Stocks'), pr.number_of_stocks_string_formatted())
        elif pr.role in ('IN', 'IF', 'IV', 'IA'):
            return '%s = %s' % (_('Amount of Investment (M rls)'), pr.amount_of_investment_string_formatted())
        else:
            return ''

    def person_roles(self):
        pass

    person_roles.short_description = _('Selected Natural Key Persons')

    def legal_roles(self):
        pass

    legal_roles.short_description = _('Selected Legal Key Persons')

    def person_roles_tabular(self):
        pass

    person_roles_tabular.short_description = _('Selected Natural Key Persons')

    def legal_roles_tabular(self):
        pass

    legal_roles_tabular.short_description = _('Selected Legal Key Persons')

    @property
    def total_news(self):
        pass

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

    def total_investment_string_formatted(self):
        return super().total_investment_string_formatted()

    total_investment_string_formatted.short_description = Person.total_investment_string_formatted.short_description

    def total_purchased_stocks_string_formatted(self):
        return super().total_purchased_stocks_string_formatted()

    total_purchased_stocks_string_formatted.short_description = Person.total_purchased_stocks_string_formatted.short_description

    def total_fund_string_formatted(self):
        return super().total_fund_string_formatted()

    total_fund_string_formatted.short_description = Person.total_fund_string_formatted.short_description

    def total_sold_stocks_string_formatted(self):
        return super().total_sold_stocks_string_formatted()

    total_sold_stocks_string_formatted.short_description = Person.total_sold_stocks_string_formatted.short_description

    def total_investment_tabular(self):
        pass

    def total_purchased_stocks_tabular(self):
        pass

    def total_fund_tabular(self):
        pass

    def total_sold_stocks_tabular(self):
        pass


class LegalPerson(LegalPersonBase):
    class Meta(LegalPersonBase.Meta):
        verbose_name = _('Legal Person')
        verbose_name_plural = _('Legal Persons')

    def __str__(self):
        return '%s: %s' % (_('Legal Person'), self.name)

    def __unicode__(self):
        return '%s: %s' % (_('Legal Person'), self.name)

    @property
    def total_news(self):
        return reduce(lambda N, n: N | n.person.total_news.all(),
                      LegalPersonLegalRole.objects.filter(target_person=self).all(),
                      reduce(lambda N, n: N | n.person.news.all(),
                             LegalPersonPersonRole.objects.filter(target_person=self).all(),
                             self.news.all()).distinct()).distinct()

    def roles_tabular(self):
        result = ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(lplr.target_person), lplr.target_person.name,
                get_admin_url(lplr.target_person), Role(lplr.role).label,
                get_admin_url(lplr.target_person), lplr.target_person.generate_comment(lplr))
            for index, lplr in enumerate(LegalPersonLegalRole.objects.filter(person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

        result += ''.join(
            '<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
                index % 2 + 1, index + 1, get_admin_url(blr.target_person), blr.target_person.name,
                get_admin_url(blr.target_person), Role(blr.role).label,
                get_admin_url(blr.target_person), blr.target_person.generate_comment(blr))
            for index, blr in enumerate(BrandLegalRole.objects.filter(person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    roles_tabular.short_description = Person.roles_tabular.short_description

    def person_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(lppr.role).label, lppr.person.name) for index, lppr in
            enumerate(LegalPersonPersonRole.objects.filter(target_person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

    person_roles.short_description = LegalPersonBase.person_roles.short_description

    def legal_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(lplr.role).label, lplr.person.name) for index, lplr in
            enumerate(LegalPersonLegalRole.objects.filter(target_person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

    legal_roles.short_description = LegalPersonBase.legal_roles.short_description

    def person_roles_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lppr.person), lppr.person.name,
            get_admin_url(lppr.person), Role(lppr.role).label,
            get_admin_url(lppr.person), lppr.target_person.generate_comment(lppr))
                         for index, lppr in enumerate(LegalPersonPersonRole.objects.filter(target_person=self).exclude(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                      Role.STOCKHOLDER])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    person_roles_tabular.short_description = LegalPersonBase.person_roles_tabular.short_description

    def legal_roles_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lplr.person), lplr.person.name,
            get_admin_url(lplr.person), Role(lplr.role).label,
            get_admin_url(lplr.person), lplr.target_person.generate_comment(lplr))
                         for index, lplr in enumerate(LegalPersonLegalRole.objects.filter(target_person=self).exclude(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                      Role.STOCKHOLDER])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    legal_roles_tabular.short_description = LegalPersonBase.legal_roles_tabular.short_description

    def total_investment(self):
        result = 0
        roles = LegalPersonLegalRole.objects.filter(person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        roles = BrandLegalRole.objects.filter(person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        return result

    def total_purchased_stocks(self):
        result = 0
        roles = LegalPersonLegalRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        roles = BrandLegalRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        return result

    def total_fund(self):
        result = 0
        roles = LegalPersonPersonRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        roles = LegalPersonLegalRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        return result

    def total_sold_stocks(self):
        result = 0

        roles = LegalPersonPersonRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        roles = LegalPersonLegalRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        return result

    def total_investment_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lplr.target_person), lplr.target_person.name,
            get_admin_url(lplr.target_person), Role(lplr.role).label,
            get_admin_url(lplr.target_person), lplr.target_person.generate_comment(lplr))
                         for index, lplr in enumerate(LegalPersonLegalRole.objects.filter(person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        result += ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(blr.target_person), blr.target_person.name,
            get_admin_url(blr.target_person), Role(blr.role).label,
            get_admin_url(blr.target_person), blr.target_person.generate_comment(blr))
                          for index, blr in enumerate(BrandLegalRole.objects.filter(person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    def total_purchased_stocks_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lplr.target_person), lplr.target_person.name,
            get_admin_url(lplr.target_person), Role(lplr.role).label,
            get_admin_url(lplr.target_person), lplr.target_person.generate_comment(lplr))
                         for index, lplr in
                         enumerate(LegalPersonLegalRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)))

        result += ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(blr.target_person), blr.target_person.name,
            get_admin_url(blr.target_person), Role(blr.role).label,
            get_admin_url(blr.target_person), blr.target_person.generate_comment(blr))
                          for index, blr in
                          enumerate(BrandLegalRole.objects.filter(person=self).filter(role=Role.STOCKHOLDER)))
        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    def total_fund_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lppr.person), lppr.person.name,
            get_admin_url(lppr.person), Role(lppr.role).label,
            get_admin_url(lppr.person), self.generate_comment(lppr))
                         for index, lppr in enumerate(LegalPersonPersonRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        result += ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lplr.person), lplr.person.name,
            get_admin_url(lplr.person), Role(lplr.role).label,
            get_admin_url(lplr.person), self.generate_comment(lplr))
                          for index, lplr in enumerate(LegalPersonLegalRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)

        return mark_safe(result)

    def total_sold_stocks_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lppr.person), lppr.person.name,
            get_admin_url(lppr.person), Role(lppr.role).label,
            get_admin_url(lppr.person), self.generate_comment(lppr))
                         for index, lppr in enumerate(
            LegalPersonPersonRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)))

        result += ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(lplr.person), lplr.person.name,
            get_admin_url(lplr.person), Role(lplr.role).label,
            get_admin_url(lplr.person), self.generate_comment(lplr))
                          for index, lplr in enumerate(
            LegalPersonLegalRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)

        return mark_safe(result)


class Brand(LegalPersonBase):
    logo = ResizedImageField(size=[settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT],
                             verbose_name=_('Logo'), upload_to='media/', blank=True, null=True)

    class Meta(LegalPersonBase.Meta):
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

    @property
    def total_news(self):
        return reduce(lambda N, n: N | n.person.total_news.all(),
                      BrandLegalRole.objects.filter(target_person=self).all(),
                      reduce(lambda N, n: N | n.person.news.all(),
                             BrandPersonRole.objects.filter(target_person=self).all(),
                             self.news.all()).distinct()).distinct()

    def person_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(bpr.role).label, bpr.person.name) for index, bpr in
            enumerate(BrandPersonRole.objects.filter(target_person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

    person_roles.short_description = LegalPersonBase.person_roles.short_description

    def legal_roles(self):
        return ' - '.join(
            '{}: {}'.format(Role(blr.role).label, blr.person.name) for index, blr in
            enumerate(BrandLegalRole.objects.filter(target_person=self).exclude(
                role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                          Role.STOCKHOLDER])))

    legal_roles.short_description = LegalPersonBase.legal_roles.short_description

    def person_roles_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(bpr.person), bpr.person.name,
            get_admin_url(bpr.person), Role(bpr.role).label,
            get_admin_url(bpr.person), bpr.target_person.generate_comment(bpr))
                         for index, bpr in enumerate(BrandPersonRole.objects.filter(target_person=self).exclude(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                      Role.STOCKHOLDER])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    person_roles_tabular.short_description = LegalPersonBase.person_roles_tabular.short_description

    def legal_roles_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(blr.person), blr.person.name,
            get_admin_url(blr.person), Role(blr.role).label,
            get_admin_url(blr.person), blr.target_person.generate_comment(blr))
                         for index, blr in enumerate(BrandLegalRole.objects.filter(target_person=self).exclude(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC,
                      Role.STOCKHOLDER])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)
        return mark_safe(result)

    legal_roles_tabular.short_description = LegalPersonBase.legal_roles_tabular.short_description

    def total_fund(self):
        result = 0
        roles = BrandPersonRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        roles = BrandLegalRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])
        if roles.count():
            result += roles.aggregate(amount_of_investment=Sum('amount_of_investment'))['amount_of_investment']

        return result

    def total_fund_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(bpr.person), bpr.person.name,
            get_admin_url(bpr.person), Role(bpr.role).label,
            get_admin_url(bpr.person), self.generate_comment(bpr))
                         for index, bpr in enumerate(BrandPersonRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        result += ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(blr.person), blr.person.name,
            get_admin_url(blr.person), Role(blr.role).label,
            get_admin_url(blr.person), self.generate_comment(blr))
                          for index, blr in enumerate(BrandLegalRole.objects.filter(target_person=self).filter(
            role__in=[Role.INVESTOR, Role.INVESTOR_ANGEL, Role.INVESTOR_FOREIGN, Role.INVESTOR_VC])))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)

        return mark_safe(result)

    def total_sold_stocks(self):
        result = 0

        roles = BrandPersonRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        roles = BrandLegalRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)
        if roles.count():
            result += roles.aggregate(total_stocks=Sum('number_of_stocks'))['total_stocks']

        return result

    def total_sold_stocks_tabular(self):
        result = ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(bpr.person), bpr.person.name,
            get_admin_url(bpr.person), Role(bpr.role).label,
            get_admin_url(bpr.person), self.generate_comment(bpr))
                         for index, bpr in enumerate(
            BrandPersonRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)))

        result += ''.join('<tr class="row{}"><td>{}</td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td><td><a href="{}">{}</a></td></tr>'.format(
            index % 2 + 1, index + 1, get_admin_url(blr.person), blr.person.name,
            get_admin_url(blr.person), Role(blr.role).label,
            get_admin_url(blr.person), self.generate_comment(blr))
                          for index, blr in enumerate(
            BrandLegalRole.objects.filter(target_person=self).filter(role=Role.STOCKHOLDER)))

        if result:
            result = '<table><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % \
                     (_('Name'), _('Role'), _('Comment'), result)

        return mark_safe(result)


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
