from django.urls import reverse_lazy
from django.views.generic import FormView

from infrastructure.services.ip import IPService
from presentation.forms.honeypot.forms import LoginForm


class HoneypotLoginView(FormView):
    form_class = LoginForm
    template_name = "honeypot/login.html"
    success_url = reverse_lazy("honeypot-login")
    IP_service: IPService = IPService()

    def form_valid(self, form):
        form.instance.user_agent = self.request.META.get('HTTP_USER_AGENT')
        form.instance.ip = self.IP_service.get_client_ip(self.request)
        form.instance.session_key = self.request.session.session_key
        form.instance.path = self.request.path
        form.save()
        return super().form_valid(form)
