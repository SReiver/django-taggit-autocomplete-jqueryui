# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('taggit_autocomplete_jqueryui.views',
    url(r'^json$', 'tag_list_view',
            name='taggit_autocomplete_jqueryui_tag_list'),
)
