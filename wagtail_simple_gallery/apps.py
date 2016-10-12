from __future__ import unicode_literals

from django.apps import AppConfig


class WagtailSimpleGalleryConfig(AppConfig):
    name = 'wagtail_simple_gallery'

    def ready(self):
        import wagtail_simple_gallery.wagtail_hooks
