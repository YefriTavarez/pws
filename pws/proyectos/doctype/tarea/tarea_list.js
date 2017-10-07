frappe.listview_settings["Tarea"] = {
	hide_name_column: true,
	add_fields: ["project_name", "project", "status", "name", "owner"],
	onload: function(list, html, doc) {
		frappe.route_options = {
			"status": ["!=", "Closed"],
			"user": ["=", frappe.session.user]
		}
	},
	post_render_item: function(list, html, doc) {
		if (doc.owner != frappe.session.user && ! frappe.user.has_role("Supervisor de Proyectos")) {
			$(html).hide()
		}

		var indicators = {
			"Open": "blue",
			"Working": "blue",
			"Pending Review": "orange",
			"Overdue": "red",
			"Closed": "green",
			"Cancelled": "grey",
		}
		var $row = $(html)

		var indicator = __("<span title='{0}' class='indicator {1}'></span>", 
			[doc.status, indicators[doc.status]])

		$row.find('a[data-filter^=subject]')
			.prepend(indicator)

		$row.find('a[data-filter^=subject]').on("click", function(event) {
			frappe.set_route(["Form", "Tarea", doc.name])

			event.stopPropagation()
		})


		$row.find('a[class="grey list-id  ellipsis"]').attr("href", "#Form/Proyecto/" + doc.project)
			.on("click", function(event) {
				frappe.set_route(["Form", "Proyecto", doc.project])
				event.stopPropagation()
			})

	}
}