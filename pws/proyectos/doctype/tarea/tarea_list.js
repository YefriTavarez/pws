frappe.listview_settings["Tarea"] = {
	hide_name_column: true,
	add_fields: ["project_name", "project", "status", "name", "owner", "dependant", "exp_end_date"],
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
		var $row = $(html)
		var fmt = "YYYY-MM-DD HH:mm:ss"

		if (doc.owner != frappe.session.user && ! frappe.user.has_role("Supervisor de Proyectos")) {
			$(html).hide()

			return ;
		}

		var indicators = {
			"Open": "blue",
			"Working": "darkgrey",
			"Pending Review": "orange",
			"Overdue": "red",
			"Closed": "green",
			"Cancelled": "grey",
		}

		var request = {
		    "method": "pws.has_any_open"
		}
		
		request.args = {
			"task": doc.name
		}
		
		request.callback = function(response) {
			var has_any_open = response.message['has_any_open']

			if (doc.dependant && ! flt(has_any_open)) {
				indicators["Open"] = "orange"
			}

			$row.find('a[data-filter^=subject]').prepend(
				__("<span title='{0}' class='indicator {1}'></span>", [doc.status, 
			indicators[doc.status]]))
		}
		
		frappe.call(request)

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

