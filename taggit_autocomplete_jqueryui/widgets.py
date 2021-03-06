# -*- coding: utf-8 -*-
from django.forms.widgets import Input
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from taggit.utils import edit_string_for_tags, split_strip
from taggit.models import Tag

MEDIA_URL = '/media/taggit_autocomplete_jqueryui'


class TagAutocomplete(Input):

    class Media:
        css = {
            'all': (
                'taggit_autocomplete_jqueryui/css/jquery-ui.css',
                'taggit_autocomplete_jqueryui/css/autocomplete.css',
            )
        }
        js = (
            'taggit_autocomplete_jqueryui/js/jquery-ui-1.11.4.min.js',
            'taggit_autocomplete_jqueryui/js/autocomplete.1.2.js',
        )

    def use_required_attribute(self, initial):
        return False

    def render(self, name, value, attrs=None):
        attrs.update({"class": "hidden"})
        tags = []
        if value is not None and not isinstance(value, basestring):
            # value contains a list a TaggedItem instances
            # Here we retrieve a comma-delimited list of tags
            # suitable for editing by the user
            tags = [o.tag for o in value.select_related('tag')]
            value = edit_string_for_tags(tags)
        elif value is not None:
            tags = [Tag(name=n.replace('"', '')) for n in split_strip(value)]

        json_view = reverse('taggit_autocomplete_jqueryui_tag_list')

        html = u'<div class="selector"><ul class="tags">'
        for tag in tags:
            html += (u'''
                <li data-tag="%(name)s">
                    <span class="name">%(name)s</span>
                    <a class="remove" href="#">X</a>
                </li>''' % {'name': tag.name})
        html += '</ul>'
        html += super(TagAutocomplete, self).render(name, value, attrs)
        html += u'<input type="text" id="%s_autocomplete"/></div>' % attrs['id']

        js = u'''
            <script type="text/javascript">
                (function (root) {
                    root.taggit_init = root.taggit_init || [];
                    root.taggit_init.push(['#%s_autocomplete', '%s']);
                })(window);
            </script>''' % (attrs['id'], json_view)
        return mark_safe("\n".join([html, js]))

