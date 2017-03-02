# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = [
    url(r'^json$', 'tag_list_view',
            name='taggit_autocomplete_jqueryui.views.taggit_autocomplete_jqueryui_tag_list'),
]
