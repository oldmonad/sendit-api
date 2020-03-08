from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = "sendit.apps.authentication"
    label = "authentication"
    verbose_name = "Authentication"

    def ready(self):
        import sendit.apps.authentication.signals


default_app_config = "sendit.apps.authentication.AuthenticationAppConfig"
