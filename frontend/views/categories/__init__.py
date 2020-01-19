from django.urls import reverse

from frontend.constants import (CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY,
                                CATEGORY_DELETED_SUCCESSFULLY,
                                CATEGORY_DOES_NOT_EXIST)
from frontend.custom.decorators import is_authenticated, is_allowed
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import delete_model
from frontend.custom.views import TandoraListViewMixin
from frontend.forms.categories import CategoryForm
from v1.categories.models import Category


@is_authenticated
@is_allowed('categories')
def category_form(request):
    return TandoraForm(Category, CategoryForm, 'create', 'staff/form.html',
                       '/')\
        .get_form(request, success_message=CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=CATEGORY_DOES_NOT_EXIST)


@is_authenticated
def edit_category(request, id):
    return TandoraForm(Category, CategoryForm, 'edit', 'staff/form.html',
                       '/')\
        .get_form(request,
                  success_message=CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=CATEGORY_DOES_NOT_EXIST, id=id)


@is_authenticated
def delete_category(request, id):
    return delete_model(request, Category, id, reverse('frontend-view-categories'), '/', CATEGORY_DELETED_SUCCESSFULLY,
                        CATEGORY_DOES_NOT_EXIST)


class CategoryList(TandoraListViewMixin):
    template_name = 'staff/categories/index.html'

    def get_queryset(self):
        company_id = self.request.session['company-id']
        return Category.objects.filter(company__id=company_id, deleted=False)
