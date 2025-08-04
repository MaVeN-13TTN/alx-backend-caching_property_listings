from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "properties"

    def ready(self):
        """
        Import signal handlers when Django starts.

        This method is called when the app is ready and ensures that
        our signal handlers are registered and will be triggered when
        Property model instances are saved or deleted.
        """
        import properties.signals  # noqa: F401
