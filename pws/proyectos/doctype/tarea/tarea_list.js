frappe.listview_settings["Tarea"] = {
	hide_name_column: true,
	add_fields: ["project_name", "project", "status", "name", "owner"],
	hide_sidebar: true,
	onload: function(list, html, doc) {
		frappe.route_options = {
			"status": ["!=", "Closed"],
			"user": ["=", frappe.session.user]
		}
	},
	post_render: function(list, html, doc) {
		// hide things
		list.page.sidebar.hide()
		list.page.fields_dict.name.$wrapper.hide()

		var parent = list.page.body.parent()

		parent.removeClass("col-md-10 layout-main-section-wrapper")
			.removeClass("col-md-12 layout-main-section-wrapper")

		list.page.fields_dict.project.get_query = function() {
			return {
				"filters": {
					"status": "Open"
				}
			}
		}
	},
	post_render_item: function(list, html, doc) {
		// doc._hide_activity = true
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