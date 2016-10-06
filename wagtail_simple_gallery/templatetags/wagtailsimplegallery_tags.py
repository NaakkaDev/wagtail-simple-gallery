from __future__ import absolute_import, unicode_literals

from django import template

from wagtail_simple_gallery.models import get_gallery_images

register = template.Library()


@register.inclusion_tag('wagtail_simple_gallery/simple_gallery.html')
def simple_gallery(tags=None, image_limit=None, use_lightbox=True):
    images = None
    try:
        images = get_gallery_images(tags.split() if tags else None)
        if image_limit:
            images = images[:image_limit]
    except:
        pass
    return {'gallery_images': images, 'use_lightbox': use_lightbox}
