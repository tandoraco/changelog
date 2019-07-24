from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from frontend.constants import CATEGORY_CREATED_SUCCESSFULLY
from frontend.forms.categories import CategoryForm


def category_form(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)

        if form.is_valid():
            category = form.save()
            messages.success(request, CATEGORY_CREATED_SUCCESSFULLY.format(category.name))
            return HttpResponseRedirect('/')
    else:
        form = CategoryForm()

    return render(request, 'category-form.html', {'form': form})
