// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Configuracion General', {
	refresh: function(frm) {
		var events = ["set_queries"]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	set_queries: function(frm) {
		var queries = ["set_item_group_query", 
			"materials_item_group_query"]

		$.map(queries, function(query) {
			frm.trigger(query)
		})
	},
	set_item_group_query: function(frm) {
		var filters = {
			"is_group": "1"
		}

		frm.set_query("item_group", function() {
			return {
				"filters": filters
			}
		})
	},
	materials_item_group_query: function(frm) {
		var filters = {
			"parent_item_group": "All Item Groups"
		}

		frm.set_query("materials_item_group", function() {
			return {
				"filters": filters
			}
		})	
	}
})
