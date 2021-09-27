from django.http import Http404

from frontend.constants import CHANGELOG_DOES_NOT_EXIST_ERROR, CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY, \
    CHANGELOG_DELETED_SUCCESSFULLY
from frontend.custom.decorators import is_authenticated, is_allowed
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import delete_model
from frontend.forms.core.changelog import ChangelogForm
from v1.core.models import Changelog
from v1.integrations.background_tasks import trigger_integration_background_tasks


def changelog_form(request, action, instance=None):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['company'] = request.user.company.id
    else:
        post_data = None
    data = {'request': request}
    post_commit_data = {
        'created_by_id': request.user.id,
        'last_edited_by_id': request.user.id
    }
    if action != 'create':
        post_commit_data.pop('created_by_id')
    return TandoraForm(Changelog, ChangelogForm, action, 'staff_v2/postlogin_form.html',
                       '/', initial=data) \
        .get_form(request, success_message=CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=CHANGELOG_DOES_NOT_EXIST_ERROR, post_data=post_data, is_multipart_form=True,
                  post_commit_data=post_commit_data, instance=instance,
                  post_save_callback=trigger_integration_background_tasks)


@is_authenticated
@is_allowed('changelogs')
def edit_changelog(request, id):
    try:
        company_id = request.session["company-id"]
        changelog = Changelog.objects.get(company__id=company_id, pk=id, deleted=False)
        return changelog_form(request, 'edit', instance=changelog)
    except Changelog.DoesNotExist:
        raise Http404


@is_authenticated
@is_allowed('changelogs')
def create_changelog(request):
    return changelog_form(request, 'create')


@is_authenticated
def delete_changelog(request, id):
    return delete_model(request, Changelog, id, '/', '/', CHANGELOG_DELETED_SUCCESSFULLY,
                        CHANGELOG_DOES_NOT_EXIST_ERROR)
