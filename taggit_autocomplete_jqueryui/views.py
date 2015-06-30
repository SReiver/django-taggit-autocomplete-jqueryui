# -*- coding: utf-8 -*-
import json
from django.db.models.loading import cache
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings


def tag_list_view(request):
    if not hasattr(settings,'TAGGIT_AUTOCOMPLETE_TAG_MODEL'):
        settings.TAGGIT_AUTOCOMPLETE_TAG_MODEL = 'taggit.Tag'
    app_label, model_class = TAGGIT_AUTOCOMPLETE_TAG_MODEL.split('.')
    Tag = cache.get_model(app_label, model_class)
    try:
        tags = (Tag.objects.
                filter(name__istartswith=request.GET['term']).
                values_list('name', flat=True))
    except MultiValueDictKeyError:
        tags = []
    return HttpResponse(json.dumps(list(tags), ensure_ascii=False),
            mimetype='application/json')
