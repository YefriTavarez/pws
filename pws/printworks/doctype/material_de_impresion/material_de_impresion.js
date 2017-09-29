// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt


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
			frm.is_new() ? "default_material_item_group": ""
		]

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
	item_group_1: function(frm) {
		frm.set_value("item_group_2", "")
	},
	item_group_2: function(frm) {
		frm.set_value("item_group_3", "")
	},
	item_group_3: function(frm) {
		frm.set_value("item_group_4", "")
	},
	item_group_4: function(frm) {
		// to do
	},
})
