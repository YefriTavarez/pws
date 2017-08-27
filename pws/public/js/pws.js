$(document).ready(function(event) {
	// hide the help menu
	$(".dropdown.dropdown-help.dropdown-mobile").hide()

	$.extend(frappe.app, {
		refresh_notifications: refresh_notifications
	})
})

var refresh_notifications = function() {
	var me = this;
	if (frappe.session_alive) {
		return frappe.call({
			method: "frappe.desk.notifications.get_notifications",
			callback: function callback(r) {
				if (r.message) {
					$.extend(frappe.boot.notification_info, r.message);
					$(document).trigger("notification-update");

					me.update_notification_count_in_modules();

					if (frappe.get_route()[0] != "messages") {
						if (r.message.new_messages.length) {
							frappe.utils.set_title_prefix("(" + r.message.new_messages.length + ")");
						}
					}
				}
			},
			freeze: false,
			type: "GET"
		});
	}
}

_f.Frm.prototype.is_new = function () {
	return this.doc && this.doc.__islocal;
};
