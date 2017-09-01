frappe.listview_settings["Proyecto"] = {
	onload: function(listview) {
		frappe.route_options = {
			"status": "Open"
		}
	}
}