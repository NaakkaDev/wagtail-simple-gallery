from django.apps import AppConfig


class WagtailSimpleGalleryConfig(AppConfig):
    name = 'wagtail_simple_gallery'
    verbose_name = "Wagtail Simple Gallery"
    verbose_name_plural = "Wagtail Simple Galleries"

    def ready(self):
        import wagtail_simple_gallery.wagtail_hooks
