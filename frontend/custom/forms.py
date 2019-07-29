from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

ACTION_CREATE = "create"
ACTION_EDIT = "edit"


class TandoraForm:

    def __init__(self, model, form, action, form_html, response_redirect, serializer=None):
        self.model = model
        self.form = form
        self.action = action
        self.form_html = form_html
        self.response_redirect_path = response_redirect
        self.serializer = serializer

    def _get_instance(self, id, request, error_message):
        try:
            instance = self.model.objects.get(id=id)
            return instance
        except self.model.Does.NotExist:
            messages.error(request, error_message)
            return HttpResponseRedirect(self.response_redirect_path)

    def get_form(self, request, success_message, error_message, id=None):
        form = self.form()

        if id:
            form = self.form(instance=self._get_instance(id, request, error_message))

        if request.method == 'POST':

            if self.action == ACTION_CREATE:
                form = self.form(request.POST)

            if self.action == ACTION_EDIT:
                if not id:
                    raise RuntimeError("Form edit. Id not provided")

                form = self.form(request.POST, instance=self._get_instance(id, request, error_message))

            if form.is_valid():
                obj = form.save()
                messages.success(request, message=success_message.format(self.action, obj.id))
                return HttpResponseRedirect(self.response_redirect_path)

        return render(request, self.form_html,
                      {'form': form, 'title': self.action.title()})
