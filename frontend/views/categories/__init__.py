from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from frontend.constants import CATEGORY_CREATED_SUCCESSFULLY, CATEGORY_DELETED_SUCCESSFULLY
from frontend.custom.views import TandoraListViewMixin
from frontend.forms.categories import CategoryForm
from v1.categories.models import Category


def category_form(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)

        if form.is_valid():
            category = form.save()
            messages.success(request, CATEGORY_CREATED_SUCCESSFULLY.format(category.name))
            return HttpResponseRedirect('/manage/categories')
    else:
        form = CategoryForm()

    return render(request, 'category-form.html', {'form': form})


def edit_category(request, id):
    return HttpResponseRedirect('/manage/categories')


def delete_category(request, id):
    try:
        category = Category.objects.get(id=id)
        category.deleted = True
        category.save()

        messages.success(request, message=CATEGORY_DELETED_SUCCESSFULLY)
    except Category.DoesNotExist:
        return HttpResponseRedirect('/')

    return HttpResponseRedirect('/manage/categories')


class CategoryList(TandoraListViewMixin):
    template_name = 'category-items.html'

    def get_queryset(self):
        return Category.objects.filter(deleted=False)
