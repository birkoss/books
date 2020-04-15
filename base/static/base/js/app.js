jQuery(document).ready(function() {
	var path = window.location.href;

	jQuery("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
		if (this.href === path) {
			jQUery(this).addClass("active");
		}
	});

	jQuery("#sidebarToggle").on("click", function(e) {
		e.preventDefault();
		jQuery("body").toggleClass("sb-sidenav-toggled");
	});
});