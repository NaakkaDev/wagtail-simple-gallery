from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from taggit.managers import TaggableManager
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, CollectionMember
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailsearch import index


class CustomImage(AbstractImage):
    show_in_gallery = models.BooleanField(default=False)

    admin_form_fields = Image.admin_form_fields + (
        'show_in_gallery',
    )

    search_fields = CollectionMember.search_fields + [
        index.SearchField('title', partial_match=True, boost=10),
        index.RelatedFields('tags', [
            index.SearchField('name', partial_match=True, boost=10),
        ]),
        index.FilterField('uploaded_by_user'),
        index.FilterField('show_in_gallery'),
    ]

    def original_url(self):
        return os.path.join(settings.MEDIA_URL, str(self.file))


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


@receiver(post_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(post_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class SimpleGalleryIndex(Page):
    intro_title = models.CharField(
        max_length=250,
        blank=True,
        help_text='Optional H1 title for the page.'
    )
    intro_text = RichTextField(
        blank=True,
        help_text='Optional text to go with the intro text.'
    )
    images_per_page = models.IntegerField(
        default=8,
        help_text='How many images there should be on one page.'
    )
    use_lightbox = models.BooleanField(
        default=True,
        help_text='Use lightbox to view larger images when clicking the thumbnail.'
    )
    tags = TaggableManager(
        blank=True,
        help_text='Only show images with certain tags. Show all if empty.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_title', classname='full title'),
        FieldPanel('intro_text', classname='full title'),
        FieldPanel('images_per_page', classname='full title'),
        FieldPanel('use_lightbox'),
        FieldPanel('tags'),
    ]

    @property
    def images(self):
        return get_gallery_images(self.tags.names())

    def get_context(self, request):
        images = self.images

        tag = request.GET.get('tag')
        if tag:
            images = images.filter(tags__name=tag)

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


def get_gallery_images(tag_list):
    images = None
    try:
        images = CustomImage.objects.filter(show_in_gallery=True).order_by('-created_at')
    except:
        pass
    if images and tag_list:
        images = images.filter(tags__name__in=tag_list).distinct()
    return images
