from __future__ import absolute_import, unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image


class SimpleGalleryIndex(Page):
    intro_title = models.CharField(
        max_length=250,
        blank=True,
        help_text='Optional H1 title for the gallery page.'
    )
    intro_text = RichTextField(
        blank=True,
        help_text='Optional text to go with the intro text.'
    )
    collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Show images in this collection in the gallery view.'
    )
    images_per_page = models.IntegerField(
        default=8,
        help_text='How many images there should be on one page.'
    )
    use_lightbox = models.BooleanField(
        default=True,
        help_text='Use lightbox to view larger images when clicking the thumbnail.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_title', classname='full title'),
        FieldPanel('intro_text', classname='full title'),
        FieldPanel('collection'),
        FieldPanel('images_per_page', classname='full title'),
        FieldPanel('use_lightbox'),
    ]

    @property
    def images(self):
        return get_gallery_images(self.collection.name)

    def get_context(self, request):
        images = self.images
        page = request.GET.get('page')
        paginator = Paginator(images, self.images_per_page)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        context = super(SimpleGalleryIndex, self).get_context(request)
        context['gallery_images'] = images
        return context


def get_gallery_images(collection, tags=None):
    images = None
    try:
        images = Image.objects.filter(collection__name=collection).order_by('-created_at')
    except Exception as e:
        pass
    if images and tags:
        images = images.filter(tags__name__in=tags).distinct()
    return images
