from django.views.generic import ListView

from frontend.views.auth.mixins import LoginRequiredMixin, IsAdmin


class TandoraListViewMixin(LoginRequiredMixin, ListView):
    pass


class TandoraAdminListViewMixin(IsAdmin, ListView):
    pass
