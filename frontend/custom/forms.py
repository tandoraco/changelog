from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from v1.audit.actions import AuditLogAction

ACTION_CREATE = "create"
ACTION_EDIT = "edit"
ID_NOT_PROVIDED_ERROR = "Form edit. Id not provided"
ID_OR_INSTANCE_NOT_PROVIDED_ERROR = "Form edit. Either ID or instance is required."


class TandoraForm:

    def __init__(self, model, form, action, form_html, response_redirect, serializer=None, initial=None):
        self.model = model
        self.form = form
        self.action = action
        self.form_html = form_html
        self.response_redirect_path = response_redirect
        self.serializer = serializer
        self.initial = initial

    def _get_instance(self, id, request, error_message):
        try:
            if hasattr(self.model, "company"):
                company_id = request.session['company-id']
                if hasattr(self.model, 'deleted'):
                    return self.model.objects.get(company__id=company_id, id=id, deleted=False)
                return self.model.objects.get(company__id=company_id, id=id)
            elif hasattr(self.model, 'deleted'):
                return self.model.objects.get(id=id, deleted=False)
            else:
                return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            raise Http404

    def get_form(self, request, success_message=None, error_message=None, id=None, extra=None,
                 title=None, post_data=None, instance=None, is_multipart_form=False,
                 update_file_in_company=None):
        form = self.form() if not self.initial else self.form(initial=self.initial)

        if not success_message:
            success_message = self.model.__name__.title() + ' {}ed successfully : {}'

        if not error_message:
            error_message = f'{self.model.__name__.title()} does not exist.'

        if id:
            form = self.form(instance=self._get_instance(id, request, error_message))
        if instance:
            id = instance.id
            form = self.form(instance=instance)

        if not title:
            title = f'{self.action.title()} {self.model.__name__}'

        if request.method == 'POST':

            if self.action == ACTION_CREATE:
                form = self.form(post_data or request.POST, request.FILES or None)

            if self.action == ACTION_EDIT:
                if not (id or instance):
                    raise RuntimeError(ID_OR_INSTANCE_NOT_PROVIDED_ERROR)

                post_data = request.POST.copy()
                post_data["id"] = id
                form = self.form(post_data, request.FILES or None,
                                 instance=self._get_instance(id, request, error_message))

            if form.is_valid():
                try:
                    obj = form.save(commit=False)

                    if self.action == ACTION_CREATE and hasattr(self.model, "company"):
                        setattr(obj, "company_id", request.session['company-id'])

                    obj.save()
                except TypeError:  # This happens, when the passed form is not a ModelForm
                    obj = form.save()

                try:
                    AuditLogAction(request, obj, 'ui').set_audit_log(self.action)
                except AttributeError:
                    pass

                if request.FILES and update_file_in_company and hasattr(obj, update_file_in_company):
                    fil = getattr(obj, update_file_in_company)
                    file_path_url = fil.url
                    company_settings = request.user.company.settings
                    company_settings[f'company_{update_file_in_company}'] = file_path_url
                    request.user.company.settings = company_settings
                    request.user.company.save()

                messages.success(request, message=success_message.format(self.action, str(obj)))
                return HttpResponseRedirect(self.response_redirect_path)

        return render(request, self.form_html,
                      {'form': form, 'title': title, 'extra': extra, 'is_multipart_form': is_multipart_form})
