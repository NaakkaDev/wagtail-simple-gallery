from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image


IMAGE_ORDER_TYPES = (
    (1, 'Image title'),
    (2, 'Newest image first'),
)


class SimpleGalleryIndex(Page):
    intro_title = models.CharField(
        verbose_name=_('Intro title'),
        max_length=250,
        blank=True,
        help_text=_('Optional H1 title for the gallery page.')
    )
    intro_text = RichTextField(
        blank=True,
        verbose_name=_('Intro text'),
        help_text=_('Optional text to go with the intro text.')
    )
    collection = models.ForeignKey(
        'wagtailcore.Collection',
        verbose_name=_('Collection'),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Show images in this collection in the gallery view.')
    )
    images_per_page = models.IntegerField(
        default=8,
        verbose_name=_('Images per page'),
        help_text=_('How many images there should be on one page.')
    )
    use_lightbox = models.BooleanField(
        verbose_name=_('Use lightbox'),
        default=True,
        help_text=_('Use lightbox to view larger images when clicking the thumbnail.')
    )
    order_images_by = models.IntegerField(choices=IMAGE_ORDER_TYPES, default=1)

    content_panels = Page.content_panels + [
        FieldPanel('intro_title', classname='full title'),
        FieldPanel('intro_text', classname='full title'),
        FieldPanel('collection'),
        FieldPanel('images_per_page', classname='full title'),
        FieldPanel('use_lightbox'),
        FieldPanel('order_images_by'),
    ]

    @property
    def images(self):
        return get_gallery_images(self.collection.name, self)

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

    class Meta:
        verbose_name = _('Gallery index')
        verbose_name_plural = _('Gallery indices')

    template = getattr(settings, 'SIMPLE_GALLERY_TEMPLATE', 'wagtail_simple_gallery/simple_gallery_index.html')


def get_gallery_images(collection, page, tags=None):
    images = None
    try:
        images = Image.objects.filter(collection__name=collection)
        if page.order_images_by == 0:
            images = images.order_by('title')
        elif page.order_images_by == 1:
            images = images.order_by('-created_at')
    except Exception as e:
        pass
    if images and tags:
        images = images.filter(tags__name__in=tags).distinct()
    return images
