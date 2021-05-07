from django.apps import apps

from frontend.custom.decorators import is_authenticated, requires_changelog_use_case
from frontend.custom.forms import TandoraForm
from frontend.forms.settings import PublicPageForm


@is_authenticated
@requires_changelog_use_case
def manage_public_page(request):
    public_page_model = apps.get_model('v1', 'PublicPage')
    public_page, created = public_page_model.objects.get_or_create(company=request.user.company)
    title = 'Edit Public page settings'
    extra = '''<b>Personalize your public page and widget color, font and logo. Make it all yours.</b><br>
    <p style="color:red;">Modifying the settings on this page will change the appearance of your public page
    and widget.</p>
    '''
    return TandoraForm(public_page_model, PublicPageForm, 'edit', 'staff_v2/postlogin_form.html',
                       '/') \
        .get_form(request, id=public_page.id, is_multipart_form=True, extra=extra, title=title,
                  update_file_in_company_settings='logo')
