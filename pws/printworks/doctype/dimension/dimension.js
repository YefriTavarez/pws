// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dimension', {
	refresh: function(frm) {
		frm.page.show_menu()

		frm.trigger("set_queries")
	},
	set_queries: function(frm) {
		var triggers = [
			"set_category_query",
			"set_product_query"
		]

		$.each(triggers, function(idx, trigger) {

			frm.trigger(trigger)
		})
	},
	set_category_query: function(frm) {
		frm.set_query("category", function() {
			return {
				"filters": {
					"is_group": "1",
					"name": ["!=", "All Item Groups"]
				}
			}
		})
	},
	set_product_query: function(frm) {
		frm.set_query("product_type", function() {

			var filters = {
				"parent_item_group": frm.doc.category
			}

			return { "filters": filters }
		})
	},
	width: function(frm) {
		frm.trigger("calculate_area")
	},
	height: function(frm) {
		frm.trigger("calculate_area")
	},
	calculate_area: function(frm) {
		var area = flt(frm.doc.width) * flt(frm.doc.height)
		frm.set_value("area", area)
	}
})
