from django.utils.html import format_html
from django.templatetags.static import static

from wagtail.core import hooks


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/simple-gallery-admin.css'))
