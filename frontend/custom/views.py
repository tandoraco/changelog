from django.views.generic import ListView

from frontend.views.auth.mixins import LoginRequiredMixin


class TandoraListViewMixin(LoginRequiredMixin, ListView):
    pass
