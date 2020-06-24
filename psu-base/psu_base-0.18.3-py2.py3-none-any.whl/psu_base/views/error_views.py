# testing_views.py
#
#   These are views that are used for debugging or testing the status of an app
#

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.services import utility_service
from psu_base.decorators import require_authority
from psu_base.models.error import Error
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from psu_base.classes.DynamicRole import DynamicRole

log = Log()
allowable_role_list = DynamicRole().super_user()


@require_authority(allowable_role_list)
def error_list(request):
    """
    Show errors encountered in this app
    """
    # Errors from this app
    app_code = utility_service.get_app_code()
    app_errors = Error.objects.filter(app_code=app_code).exclude(status='R').exclude(status='I')

    # Paginate the results
    paginator = Paginator(app_errors, 50)
    page = request.GET.get('page', 1)
    app_errors = paginator.get_page(page)

    status_options = {'N': "New", 'I': "Ignored", 'R': "Resolved", 'W': "Watch"}

    return render(
        request, 'error/list.html',
        {
            'app_errors': app_errors,
            'status_options': status_options
        }
    )


@require_authority(allowable_role_list)
def error_status(request):
    """
    Set error status
    """
    if request.method == 'POST':
        error_id = request.POST.get('error_id')
        new_status = request.POST.get('new_status')
        if error_id and new_status:
            ee = Error.objects.get(pk=int(error_id))
            ee.status = new_status
            ee.save()
            return HttpResponse(new_status)
    return HttpResponseForbidden()
