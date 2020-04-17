jQuery(document).ready(function() {

	jQuery(".list-sortable").sortable({
		placeholder : "sortable-element-highlight",
		update: function(event, ui) {
			var items = new Array();
			jQuery('.list-sortable tr').each(function() {
				items.push(jQuery(this).data("item-id"));
			});
			jQuery.ajax({
				url: window.location.href,
				method: "POST",
				data:{
					"csrfmiddlewaretoken": AJAX_CSRF_TOKEN,
					"items": items
				},
				success: function(data) {
					console.log(data);
				}
			});
		}
	});

});