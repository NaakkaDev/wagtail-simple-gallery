# Wagtail Simple Gallery
Is an extension for Torchbox's [Wagtail CMS](https://github.com/torchbox/wagtail) for creating a simple image gallery either by creating a page using the template or a templatetag.

Current version works with Wagtail 2.8.x - 5.1.x & Django 2.2.x - 4.1.x.


## Getting started
### Install
- Install via pip `pip install wagtail-simple-gallery`.
- Add `wagtail_simple_gallery` to `INSTALLED_APPS` in your project settings.
- Run `python manage.py migrate wagtail_simple_gallery`.

### Use
- Create a new collection in Wagtail CMS: **Settings -> Collections**.
- Add or upload images to the collection.
- Create a new page using the **Gallery index** type and select the new collection.
- You are done, preview or publish the page and you should see the gallery in action.


## Features / Options
- Toggleable [Lightbox](https://feimosi.github.io/baguetteBox.js/) for viewing images.
- Show images from selected collection.
- The amount of images shown on one page (before the paginator kicks in) is changeable.
- A crude way to order the images shown on a gallery page. By default newest images are shown first, but this can be changed in the page content settings. If it's set to "Image title" then you can manually order images by inserting `[<number>]` into their title: "[00004] Cute cat".
- Tags.

## Settings
### `SIMPLE_GALLERY_TEMPLATE`
You can override the `SimpleGalleryIndex` page template with this setting. Default: `wagtail_simple_gallery/simple_gallery_index.html`

### `SIMPLE_GALLERY_ADMIN_URL_ROOT`
You can use this with the [Admin Interface](#admin-interface) if you use something other than "admin" for accessing the cms admin panel. Default: `admin`

### `SIMPLE_GALLERY_PAGE_TYPE`
The page type presented to a Wagtail CMS user can be adjusted with this setting. Default: `Gallery index`.

## Templatetags
`{% load wagtailsimplegallery_tags %}`
### `{% simple_gallery %}` inclusion tag
Uses the template **wagtail_simple_gallery/simple_gallery.html**. You can use the simple-gallery style with this tag using: `<link rel="stylesheet" href="{% static 'css/simple-gallery.css' %}">`.

- `collection` (default: None): Show images from this collection. **Required**, example: `{% simple_gallery collection="Root" %}`.
- `tags` (default: None): Filter images by their tags. Example: `{% simple_gallery tags="cats dogs" %}`.
- `image_limit` (default: None): Limit the amount of images to show. Example: `{% simple_gallery image_limit=4 %}`.
- `use_lightbox` (default: True): Use lightbox for viewing images. Example: `{% simple_gallery use_lightbox=False %}`.

### `{% img|original_url %}` filter
- Takes wagtails Image object and returns its real original url instead of the one that wagtail creates. Example: `/media/original_images/foo.jpg`.


### `{% img.alt|hide_num_order %}` filter
- Hides the first occurance of `[<number>]` in the image title. E.g "[0010] Cute cat" -> "Cute cat"


## Template
Look at **simple_gallery_index.html** template for an example or copy paste it and start modifying to make it look a part of your page. Your custom **simple_gallery_index.html** template should reside in **/templates/wagtail_simple_gallery/simple_gallery_index.html**

Or if **simple_gallery_index.html** is good enough for your use, then you can just create a **simple_gallery_base.html** in your own templates directory with the following content:
```
{% extends "base.html" %}

{% block content %}{% endblock %}
```


## Admin Interface
It is suggested to take advantage of the existing Wagtail setting:

`WAGTAILIMAGES_INDEX_PAGE_SIZE = 32`
