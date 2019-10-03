from django.views.generic import ListView

from frontend.custom.mixins import LoginRequiredMixin


class TandoraListViewMixin(LoginRequiredMixin, ListView):
    pass
