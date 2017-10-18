frappe.listview_settings["Proyecto"] = {
	hide_name_column: true,
	add_fields: ["status", "expected_end_date"],
	cols_width: {"title": 10},
	onload: function(listview) {
		frappe.route_options = {
			"status": "Open"
		}
	},
	refresh: function(list, html, doc) {
		setTimeout(function() {

			$(".list-item__content--flex-2").css({
				"flex": 650
			})
		}, 999)
	},
	post_render: function(list, html, doc) {
		list.page.sidebar.hide()
		list.page.fields_dict.name.$wrapper.hide()

		var parent = list.page.body.parent()

		parent.removeClass("col-md-10 layout-main-section-wrapper")
			.removeClass("col-md-12 layout-main-section-wrapper")

		list.page.fields_dict.customer.get_query = function() {
			return {
				"query": "pws.queries.project_customer",
				"filters": {
					"status": list.page.fields_dict.status.get_value()
				}
			}
		}

		list.page.fields_dict.item.get_query = function() {
			return {
				"query": "pws.queries.project_item",
				"filters": {
					"customer": list.page.fields_dict.customer.get_value()
				}
			}
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

		// html.find("a[data-name^='PRO']").append(first_indicator)

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