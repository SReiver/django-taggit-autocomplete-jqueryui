# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views import tag_list_view

urlpatterns = [
    url(r'^json$', tag_list_view, name='taggit_autocomplete_jqueryui_tag_list'),
]

