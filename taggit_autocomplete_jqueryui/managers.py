# coding=utf-8
from taggit.forms import TagField
from taggit.managers import TaggableManager
from django.conf import settings

from widgets import TagAutocomplete


class TaggableManagerAutocomplete(TaggableManager):
    def formfield(self, form_class=TagField, **kwargs):
        field = (super(TaggableManagerAutocomplete, self).
                 formfield(form_class, **kwargs))
        field.widget = TagAutocomplete()
        return field

    def save_form_data(self, instance, value):
        value = map(lambda v: v.strip().lower(), value)
        getattr(instance, self.name).set(*value)

if 'south' in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_ignored_fields
    except ImportError:
        pass
    else:
        add_ignored_fields(["^taggit_autocomplete_jqueryui\.managers"])
