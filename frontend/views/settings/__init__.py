from django.apps import apps

from frontend.custom.decorators import is_authenticated, requires_changelog_use_case
from frontend.custom.forms import TandoraForm
from frontend.forms.settings import PublicPageForm


@is_authenticated
@requires_changelog_use_case
def manage_public_page(request):
    public_page_model = apps.get_model('v1', 'PublicPage')
    public_page, created = public_page_model.objects.get_or_create(company=request.user.company)

    return TandoraForm(public_page_model, PublicPageForm, 'edit', 'staff/form.html',
                       '/') \
        .get_form(request, id=public_page.id)
