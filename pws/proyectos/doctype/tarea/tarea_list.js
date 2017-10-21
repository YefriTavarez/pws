frappe.listview_settings["Tarea"] = {
	hide_name_column: true,
	add_fields: ["project_name", "project", "status", "name", "owner", "dependant", "exp_end_date"],
	hide_sidebar: true,
	onload: function(list, html, doc) {
		frappe.route_options = {
			"status": ["!=", "Closed"],
			// "user": ["=", frappe.session.user]
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
		    "method": "pws.get_task_status_list"
		}
		
		request.args = {
			"task": doc.name
		}
		
		request.callback = function(response) {
			var task_list = response.message
			var status = doc.status

			if (task_list) {
				var any_open = false

				$.map(task_list, function(task) {
					if (task.status != "Closed") {
						any_open = true
					}
				})

				if (["Open", "Pending Review", "Working"].includes(status)) {
					if (doc.dependant) {
						if ( moment().format(fmt) > doc.exp_end_date && ! any_open) {
							status = "Delayed"
						} else if ( moment().format(fmt) < doc.exp_end_date && ! any_open) {
							indicators["Open"] = "orange"
						} else {
							indicators["Open"] = "blue"
						}
					} else {
						if (moment().format(fmt) > doc.exp_end_date) {
							status = "Delayed"
						}
					}
				}
			}

			var indicator = __("<span title='{0}' class='indicator {1}'></span>", 
				[status, indicators[status]])

			$row.find('a[data-filter^=subject]')
				.prepend(indicator)
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

