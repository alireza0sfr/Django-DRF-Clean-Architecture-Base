from django.apps import AppConfig


class HoneyPotConfig(AppConfig):
    label = 'honeypot'
    name = 'domain.apps.honeypot'
    verbose_name = 'honeypot'

    def ready(self):
        import infrastructure.signals.honeypot.signals
