# Wagtail Simple Gallery
Is an extension for Torchbox's [Wagtail CMS](https://github.com/torchbox/wagtail) for creating a simple image gallery either by creating a page using the `Simple Gallery Index` template or using the `{% simple_gallery %}` templatetag.

## Requirements
 - Default wagtail image model in use!

## Compability
Made and tested with Wagtail 1.5.3 and Django 1.9.9


## Quick Install
**WARNING:** If you are already using a [custom image model](http://docs.wagtail.io/en/latest/advanced_topics/images/custom_image_model.html), you cannot use this as is.

 - `pip install wagtail-simple-gallery`.
 - Add `wagtail_simple_gallery` into your `INSTALLED_APPS`.
 - `WAGTAILIMAGES_IMAGE_MODEL = 'wagtail_simple_gallery.CustomImage'` django setting.
 - Run `python manage.py migrate wagtail_simple_gallery`


## Features / Options
- Image
    - "Show in Gallery"-checkbox.
- Gallery Page
    - Toggleable [Lightbox](https://feimosi.github.io/baguetteBox.js/) for viewing images.
    - Show all images, which have 'show in gallery' checked, or only those with certain tags.
    - The amount of images shown on one page (before the paginator kicks in) is changeable.


## `{% simple_gallery %}` tag
 - `tags` (default: None): Filter images by their tags. Example: `{% simple_gallery tags="cats dogs" %}`.
 - `image_limit` (default: None): Limit the amount of images to show. Example: `{% simple_gallery image_limit=4 %}`
 - `use_lightbox` (default: True): Use lightbox for viewing images. Example: `{% simple_gallery use_lightbox=False %}`


## Template
Look at **simple_gallery_index.html** template for an example or copy paste it and start modifying to make it look a part of your page. Your custom **simple_gallery_index.html** template should reside in **/templates/wagtail_simple_gallery/simple_gallery_index.html**

Or if **simple_gallery_index.html** is good enough for your use, then you can just create a **simple_gallery_base.html** in your own templates directory with the following content:
```
{% extends "base.html" %}

{% block content %}{% endblock %}
```
