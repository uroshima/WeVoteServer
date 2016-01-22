# import_export_wikipedia/views_admin.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

from .controllers import retrieve_all_organizations_logos_from_wikipedia, retrieve_organization_logo_from_wikipedia
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from organization.models import OrganizationManager
import wevote_functions.admin
from wevote_functions.models import convert_to_int, positive_value_exists

logger = wevote_functions.admin.get_logger(__name__)


# @login_required()  # Commented out while we are developing login process()
def import_organization_logo_from_wikipedia_view(request, organization_id):
    organization_manager = OrganizationManager()
    results = organization_manager.retrieve_organization(organization_id)

    if not results['organization_found']:
        messages.add_message(request, messages.INFO, results['status'])
        return HttpResponseRedirect(reverse('organization:organization_edit', args=(organization_id,)))

    organization = results['organization']

    # When looking up logos one at a time, we want to force a retrieve
    force_retrieve = True
    results = retrieve_organization_logo_from_wikipedia(organization, force_retrieve)

    if positive_value_exists(force_retrieve):
        if 'image_options' in results:
            for one_image in results['image_options']:
                link_to_image = "<a href='{one_image}' target='_blank'>{one_image}</a>".format(one_image=one_image)
                messages.add_message(request, messages.INFO, link_to_image)

    if not results['success']:
        messages.add_message(request, messages.INFO, results['status'])
    else:
        messages.add_message(request, messages.INFO, "Wikipedia information retrieved.")

    return HttpResponseRedirect(reverse('organization:organization_position_list', args=(organization_id,)))


def retrieve_all_organizations_logos_from_wikipedia_view(request):
    results = retrieve_all_organizations_logos_from_wikipedia()

    if not results['success']:
        messages.add_message(request, messages.INFO, results['status'])
    else:
        messages.add_message(request, messages.INFO, "Wikipedia information retrieved.")

    return HttpResponseRedirect(reverse('organization:organization_list', args=()))
