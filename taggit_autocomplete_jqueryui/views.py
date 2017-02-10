# -*- coding: utf-8 -*-
import json
from django.db.models.loading import cache
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings


def tag_list_view(request):
    if not hasattr(settings,'TAGGIT_AUTOCOMPLETE_TAG_MODEL'):
        settings.TAGGIT_AUTOCOMPLETE_TAG_MODEL = 'taggit.Tag'
    app_label, model_class = settings.TAGGIT_AUTOCOMPLETE_TAG_MODEL.split('.')
    if hasattr(settings,'TAGGIT_AUTOCOMPLETE_TAG_FILTER'):
        kname, kval = settings.TAGGIT_AUTOCOMPLETE_TAG_FILTER.split('.')
        kwargs = {kname : kval }
    else:
        kwargs = {}
    Tag = cache.get_model(app_label, model_class)
    try:
        tags = (Tag.objects.
                filter(name__istartswith=request.GET['term']).filter(**kwargs).
                values_list('name', flat=True))
    except MultiValueDictKeyError:
        tags = []
    return HttpResponse(json.dumps(list(tags), ensure_ascii=False),
            content_type='application/json')
