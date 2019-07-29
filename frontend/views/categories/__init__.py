from django.urls import reverse

from frontend.constants import (CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY,
                                CATEGORY_DELETED_SUCCESSFULLY,
                                CATEGORY_DOES_NOT_EXIST)
from frontend.custom.decorators import check_auth
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import delete_model
from frontend.custom.views import TandoraListViewMixin
from frontend.forms.categories import CategoryForm
from v1.categories.models import Category


@check_auth
def category_form(request):
    return TandoraForm(Category, CategoryForm, 'create', 'category-form.html', reverse('frontend-view-categories'))\
        .get_form(request, CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY, CATEGORY_DOES_NOT_EXIST)


@check_auth
def edit_category(request, id):
    return TandoraForm(Category, CategoryForm, 'edit', 'category-form.html', reverse('frontend-view-categories'))\
        .get_form(request, CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY, CATEGORY_DOES_NOT_EXIST, id=id)


@check_auth
def delete_category(request, id):
    return delete_model(request, Category, id, reverse('frontend-view-categories'), '/', CATEGORY_DELETED_SUCCESSFULLY,
                        CATEGORY_DOES_NOT_EXIST)


class CategoryList(TandoraListViewMixin):
    template_name = 'category-items.html'

    def get_queryset(self):
        return Category.objects.filter(deleted=False)
