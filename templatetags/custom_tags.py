# -*- coding: utf8 -*-
import locale
from django import template
from django.conf import settings
import lfs.core.utils
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def currency_ru(value, request=None, grouping=True):
    """
    e.g.
    import locale
    locale.setlocale(locale.LC_ALL, 'de_CH.UTF-8')
    currency(123456.789)  # Fr. 123'456.79
    currency(-123456.789) # <span class="negative">Fr. -123'456.79</span>
    """
    
    if not value:
        value = 0.0
    
    shop = lfs.core.utils.get_default_shop(request)
    try:
        #result = locale.currency(value, grouping=grouping, international=shop.use_international_currency_code)
        result = '%s %s' % (int(value), u'руб.')
    except ValueError:
        result = value

    # add css class if value is negative
    if value < 0:
        # replace the minus symbol if needed
        if result[-1] == '-':
            length = len(locale.nl_langinfo(locale.CRNCYSTR))
            result = '%s-%s' % (result[0:length], result[length:-1])
        return mark_safe('<span class="negative">%s</span>' % result)
    return result
