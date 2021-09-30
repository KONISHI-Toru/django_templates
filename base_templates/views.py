from django.views.generic import TemplateView

class TopView(TemplateView):
    template_name = 'base/top.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
