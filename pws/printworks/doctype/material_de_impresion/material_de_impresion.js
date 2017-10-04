// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.flags")
frappe.ui.form.on('Material de Impresion', {
	refresh: function(frm) {
		var events = ["set_queries", 
			"add_custom_buttons", "toggle_enable_item_group"]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	onload_post_render: function(frm) {
		frappe.provide(__("pws.{0}", [frm.doctype]))

		var events = [
			"set_flags_for_item_groups",
			"trigger_item_groups",
		]
		
		if (frm.is_new()) {
			events.push("default_material_item_group")
		} 

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	validate: function(frm) {
		var request = {
			"method":  __("{0}.{1}", [
				frappe.model.get_server_module_name(frm.doctype),
				"rename_doc"
			])
		}
		
		request.args = {
			"frm_doc": frm.doc
		}
		
		request.callback = function(response) {
			var new_name = response.message
		
			if (new_name) {
				frappe.set_route(["Form", "Material de Impresion", new_name])
			}
		}
		
		setTimeout(function() {

			frappe.call(request)
		})
	},
	add_custom_buttons: function(frm) {
		if ( ! frm.is_new()) {
			frm.add_custom_button("Duplicar", function(event) {
				frm.copy_doc()
			})
		}
	},
	default_material_item_group: function(frm) {
		var doctype = "Configuracion General"

		var callback = function(data) {
			if (data) {
				pws[frm.doctype].default_material_group = data.materials_item_group
				frm.set_value("item_group_1", pws[frm.doctype].default_material_group)
			}
		}

		if ( ! pws[frm.doctype].default_material_group) {
			frappe.db.get_value(doctype, {
				"name": doctype 
			}, "materials_item_group", callback)
		} else {
			setTimeout(function() {
				frm.set_value("item_group_1", pws[frm.doctype].default_material_group)
			}, 999)
		}
		
		setTimeout(function() {
			var fields = ["item_group_2", "item_group_3", "item_group_4"]

			$.map(fields, function(field) {
				frm.set_value(field, undefined)
			})
		}, 1500)
	},
	toggle_enable_item_group: function(frm) {
		frm.toggle_enable("item_group_1", ! frm.doc.item_group_1)
	},
	set_flags_for_item_groups: function(frm) {
		var flags = [
			"dont_clear_item_group_2",
			"dont_clear_item_group_3",
			"dont_clear_item_group_4",
		]

		$.map(flags, function(flag) {
			pws.flags[flag] = ! frm.is_new()
		})
	},
	set_queries: function(frm) {
		var events = [
			"set_category_1_query", 
			"set_category_2_query",
			"set_category_3_query",
			"set_category_4_query"
		]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	set_category_1_query: function(frm) {
		frm.set_query("item_group_1", function() {
			var filters = {
				"parent_item_group": "All Item Groups"
			}

			return { "filters": filters }
		})
	},
	set_category_2_query: function(frm) {
		frm.set_query("item_group_2", function() {
			var filters = {
				"parent_item_group": frm.doc.item_group_1
			}
			
			return { "filters": filters }
		})
	},
	set_category_3_query: function(frm) {
		frm.set_query("item_group_3", function() {
			var filters = {
				"parent_item_group": frm.doc.item_group_2
			}
			
			return { "filters": filters }
		})
	},
	set_category_4_query: function(frm) {
		frm.set_query("item_group_4", function() {
			var filters = {
				"parent_item_group": frm.doc.item_group_3
			}
			
			return { "filters": filters }
		})
	},
	trigger_item_groups: function(frm) {
		var events = [
			"item_group_1",
			"item_group_2",
			"item_group_3",
			"item_group_4",
		]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	item_group_1: function(frm) {
		if ( ! pws.flags.dont_clear_item_group_2) {
			frm.set_value("item_group_2", "")
		}

		frappe.db.get_value("Item Group", frm.doc.item_group_1, "is_group", function(data) {
			var will_display = false

			if (data) {
				will_display = data.is_group
			}
			
			frm.toggle_display("item_group_2", will_display)
		})

		pws.flags.dont_clear_item_group_2 = undefined
	},
	item_group_2: function(frm) {
		if ( ! pws.flags.dont_clear_item_group_3) {
			frm.set_value("item_group_3", "")
		}

		frappe.db.get_value("Item Group", frm.doc.item_group_2, "is_group", function(data) {
			var will_display = false

			if (data) {
				will_display = data.is_group
			}

			frm.toggle_display("item_group_3", will_display)
		})

		pws.flags.dont_clear_item_group_3 = undefined
	},
	item_group_3: function(frm) {
		if ( ! pws.flags.dont_clear_item_group_4) {
			frm.set_value("item_group_4", "")
		}

		frappe.db.get_value("Item Group", frm.doc.item_group_3, "is_group", function(data) {
			var will_display = false

			if (data) {
				will_display =  data.is_group
			}

			frm.toggle_display("item_group_4", will_display)
		})

		pws.flags.dont_clear_item_group_4 = undefined
	},
	item_group_4: function(frm) {
		// to do
	},
	calibreopeso: function(frm) {
		var fields = [
			"calibre",
			"peso",
			"uom"
		]

		$.map(fields, function(field) {
			frm.set_value(field, "")
		})
	}
})
