from django.urls import path

from .views import index

urlpatterns = [
    # FIXME: What if wagtailadmin is located in 'cms/' URL?
    path('admin/images/', index, name='index'),
]
