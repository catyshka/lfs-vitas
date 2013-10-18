# django imports
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

# lfs imports
import lfs.customer.utils
from lfs_contact.forms import ContactForm
from lfs_contact.utils import send_contact_mail


def delivery_page(request, template_name="lfs/pages/delivery_page.html"):
    """Displays the delivery info.
    """
    return render_to_response(template_name, RequestContext(request, {}))


def order_page(request, template_name="lfs/pages/order_page.html"):
    """Displays the delivery info.
    """
    return render_to_response(template_name, RequestContext(request, {}))