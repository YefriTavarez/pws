frappe.listview_settings["Proyecto"] = {
	hide_name_column: true,
	add_fields: ["status", "expected_end_date"],
	cols_width: {"title": 10},
	onload: function(listview) {
		frappe.route_options = {
			"status": "Open"
		}
	},
	post_render_item: function(list, html, doc) {
		var title = null
		var indicators = {
			"Open": "blue",
			"Completed": "green",
			"Cancelled": "grey",
		}

		var first_indicator = __("<span title='{0}' class='indicator {1}'></span>", 
			[doc.status, indicators[doc.status]])

		// html.find("a[data-name^='PRO']").prepend(first_indicator)

		// if it's due
		if (moment() > moment(doc.expected_end_date, "YYYY-MM-DD HH:mm:ss")) {
			indicators["Open"] = "red"
			title = "Atrasado"
		}

		var second_indicator = __("<span title='{0}' class='indicator {1}'></span>", 
			[title || doc.status, indicators[doc.status]])
		
		html.find("a[data-filter^='expected_end_date']").prepend(second_indicator)
	}
}