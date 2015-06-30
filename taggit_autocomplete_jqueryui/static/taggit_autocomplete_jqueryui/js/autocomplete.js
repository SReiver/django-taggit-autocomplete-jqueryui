(function (root, $) {

	root.Taggit = (function () {
		var
			$hidden,
			$taglist;

		function updateTags (id) {
			var new_val = [];
			$taglist[id].find('li').each(function(i,el){
				new_val.push($(el).attr('data-tag'))
			});
			$hidden[id].val(new_val.join(', '));
		}

		function remove (e) {
			var $target = $(e.target).closest('.remove');
			var id = "#"+$(e.target).closest('ul').next('input').attr('id')+"_autocomplete";
			e.preventDefault();
			if ($target.length > 0) {
				$target.parent().remove();
				updateTags(id);
			}
		}

		function addTags ($input) {
			var tags = $input.val().split(',');
			var id = "#"+$input.attr('id');
			$.each(tags, function (i, tag) {
				addTagToList($.trim(tag.toLowerCase()), id);
			});
			$input.val('');
		}

		function addTagToList (tag, id) {
			if ($taglist[id].children('li[data-tag="' + tag + '"]').length === 0) {
				$taglist[id].append(
					'<li data-tag="' + tag + '">' +
						'<span class="name">' + tag + '</span>' +
						'<a href="#" class="remove">x</a>' +
					'</li>'
				);
				updateTags(id);
			}
		}

		return {
			init: function (inputSelector) {
				var $input = $(inputSelector);
				if (typeof $hidden == 'undefined')
					$hidden = {};
				$hidden[inputSelector] = $('#' + $input.attr('id').replace('_autocomplete', ''));
				if (typeof $taglist == 'undefined')
					$taglist = {};
				$taglist[inputSelector] = $hidden[inputSelector].parent().children('.tags');

				// Hooks up event listenere to enable remove
				$taglist[inputSelector].click(remove);

				// Adds enter key event on autocomplete input
				$input['keypress'](function (e) {
					if (e.keyCode === 13 || e.charCode === 44) {
						e.preventDefault();
						addTags($(e.target));
					}
				});

				// Make sure tags in the text input field are added before the form is submitted
				$($input[0].form).submit(function () {
					if ($input.val().length > 0) {
						addTags($input,'#'+$input.attr(id).replace('_autocomplete', ''));
					}
				});
			},

			autocomplete: function (e, ui) {
				e.preventDefault();
				$(e.target).val('');
				addTagToList(ui.item.value);
			}
		};
	})();

	/*
	 * Initialize a widget based on a definition containing the input element
	 * selector and the URL for the backend endpoint to retrieve tags from.
	 */
	function auto_init (selector, endpoint) {
		root.Taggit.init(selector);
        $(selector).autocomplete({
            source: endpoint,
            select: root.Taggit.autocomplete
        });
	}

	/*
	 * Check for init queue set up before this file was loaded, and
	 * run auto-initialization of each defined widget.
	 */
    if (root.taggit_init) {
        $.each(root.taggit_init, function (i, defn) {
            auto_init(defn[0], defn[1]);
        });
    }

	// Handle additions to the auto-init queue directly after this file is loaded
	root.taggit_init = {
		push: function (defn) {
			auto_init(defn[0], defn[1]);
		}
	};

})(window, window.jQuery || django.jQuery);
