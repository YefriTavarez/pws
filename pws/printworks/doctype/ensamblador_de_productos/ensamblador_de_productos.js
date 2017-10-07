// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.flags")

frappe.ui.form.on('Ensamblador de Productos', {
	refresh: function(frm) {
		var events = [
			"toggle_enable_item_group",
			"add_custom_buttons",
			"set_queries", 
			"set_flags_for_item_groups",
			"item_group_1", "item_group_2", "item_group_3",
			"show_hide_calibre_o_peso"]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	onload_post_render: function(frm) {
		frappe.provide(__("pws.{0}", [frm.doctype]))

		var events = [ "perfilador_de_productos" ]

		if (frm.is_new()) {
			events.push("default_product_item_group")
		} 

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	validate: function(frm) {
		frm.trigger("validate_duplicates")
	},
	materials: function(frm) {
		frm.trigger("show_hide_calibre_o_peso")
	},
	show_hide_calibre_o_peso: function(frm) {
		if (flt(frm.doc.material_calibre)) {
			frm.fields_dict.material_calibre.$wrapper.show()
			frm.fields_dict.material_peso.$wrapper.hide()
		}

		if (flt(frm.doc.material_peso)) {
			frm.fields_dict.material_calibre.$wrapper.hide()
			frm.fields_dict.material_peso.$wrapper.show()
		}
	},
	toggle_enable_item_group: function(frm) {
		$.map(["item_group_1", "item_group_2", "item_group_3", "item_group_4"], function(field) {
			frm.toggle_display(field, !! frm.doc.perfilador_de_productos)
		})

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
			"set_material_query",
			"set_control_query",
			"set_corte_query",
			"set_empalme_query",
			"set_plegado_query",
			"set_proteccion_query",
			"set_utilidad_query",
			"set_textura_query",
			"set_dimension_query",
			"set_category_1_query", 
			"set_category_2_query",
			"set_category_3_query",
			"set_category_4_query",
		]

		$.each(events, function(idx, event) {
			frm.trigger(event)
		})
	},
	perfilador_de_productos: function(frm) {
		if (frm.doc.perfilador_de_productos) {
			frm.trigger("fetch_the_profile_maker")
		}

		frm.trigger("toggle_enable_item_group")

		frm.refresh()
	},
	item_group_1: function(frm) {
		if ( ! pws.flags.dont_clear_item_group_2) {
			// frm.set_value("item_group_2", "")
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
			// frm.set_value("item_group_3", "")
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
			// frm.set_value("item_group_4", "")
		}

		frappe.db.get_value("Item Group", frm.doc.item_group_3, "is_group", function(data) {
			var will_display = false

			if (data) {
				will_display = data.is_group
			}
				
			frm.toggle_display("item_group_4", will_display)
		})

		pws.flags.dont_clear_item_group_4 = undefined
	},
	item_group_4: function(frm) {
		// to do
	},
	add_custom_buttons: function(frm) {
		frm.clear_custom_buttons()

		var events = [
			! frm.is_new() && "add_view_item_button"
		]

		$.each(events, function(idx, event) {
			frm.trigger(event)
		})
	},
	set_dimension_query: function(frm) {
		frm.set_query("dimension", function() {
			var query = "pws.queries.ens_dimension_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},	
	set_material_query: function(frm) {
		frm.set_query("materials", function() {
			var query = "pws.queries.ens_materials_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_control_query: function(frm) {
		frm.set_query("opciones_de_control", function() {
			var query = "pws.queries.ens_control_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	set_corte_query: function(frm) {
		frm.set_query("opciones_de_corte", function() {
			var query = "pws.queries.ens_corte_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	set_empalme_query: function(frm) {
		frm.set_query("opciones_de_empalme", function() {
			var query = "pws.queries.ens_empalme_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	set_plegado_query: function(frm) {
		frm.set_query("opciones_de_plegado", function() {
			var query = "pws.queries.ens_plegado_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	set_proteccion_query: function(frm) {
		frm.set_query("opciones_de_proteccion", function() {
			var query = "pws.queries.ens_proteccion_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	set_utilidad_query: function(frm) {
		frm.set_query("opciones_de_utilidad", "opciones_de_utilidad", function() {
			var query = "pws.queries.ens_utilidad_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	set_textura_query: function(frm) {
		frm.set_query("opciones_de_textura", "opciones_de_textura", function() {
			var query = "pws.queries.ens_textura_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos,
				"material": frm.doc.materials
			}

			return { "query": query, "filters": filters }
		})
	},
	add_view_item_button: function(frm) {
		frm.add_custom_button("Ver Item", function() {
			frm.trigger("view_item")
		})
	},
	view_item: function(frm) {
		frappe.set_route(["Form", "Item", frm.docname])
	},
	validate_duplicates: function(frm) {
		var tables = [
			"opciones_de_utilidad",
			"opciones_de_textura"
		]

		$.each(tables, function(idx, tablename) {
			pws.utils.validate_table(frm, tablename)
		})
	},
	hide_empty_fields: function(frm) {
		if (pws.profiler) {
			var fields = [
				"materials",
				"opciones_de_control",
				"opciones_de_corte",
				"opciones_de_empalme",
				"opciones_de_proteccion",
				"opciones_de_plegado",
				"opciones_de_utilidad",
				"opciones_de_textura"
			]

			$.each(fields, function(idx, fieldname) {
				var hide = !!!pws.profiler[fieldname].length

				frm.set_df_property(fieldname, "hidden", hide)
				frm.set_df_property(fieldname + "_sb", "hidden", hide)
			})

			frm.trigger("show_hide_colores")
		}
	},
	show_hide_colores: function(frm) {
		frm.set_df_property("cantidad_tiro_proceso", "hidden", !pws.profiler.tiro)
		frm.set_df_property("cantidad_tiro_pantone", "hidden", !pws.profiler.tiro)

		frm.set_df_property("cantidad_proceso_retiro", "hidden", !pws.profiler.re_tiro)
		frm.set_df_property("cantidad_pantone_retiro", "hidden", !pws.profiler.re_tiro)

		
		frm.set_df_property("colores_sb", "hidden", !pws.profiler.re_tiro && !pws.profiler.tiro)
	},
	fetch_the_profile_maker: function(frm) {
		var method = "frappe.client.get"
		
		var args = {
			"doctype": "Perfilador de Productos",
			"name": frm.doc.perfilador_de_productos
		}

		var callback = function(response) {
			var profiler = response.message

			pws.profiler = profiler
			frm.trigger("hide_empty_fields")
		}

		frappe.call({ "method": method, "args": args, "callback": callback })
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
	default_product_item_group: function(frm) {
		var doctype = "Configuracion General"

		var callback = function(data) {
			if (data) {
				pws[frm.doctype].default_product_group = data.item_group
				frm.set_value("item_group_1", pws[frm.doctype].default_product_group)
			}
		}

		if ( ! pws[frm.doctype].default_product_group) {
			frappe.db.get_value(doctype, {
				"name": doctype 
			}, "item_group", callback)
		} else {
			setTimeout(function() {
				frm.set_value("item_group_1", pws[frm.doctype].default_product_group)
			}, 999)
		}
		
		setTimeout(function() {
			var fields = ["item_group_2", "item_group_3", "item_group_4"]

			$.map(fields, function(field) {
				frm.set_value(field, undefined)
			})
		}, 1500)
	},
})

$.extend(pws.utils, {
	"has": function(key, array) {
		var found = false

		$.each(array, function(idx, value) {
			if (key == value) {
				found = true
			}
		})

		return found
	}, 
	validate_table: function(frm, tablename) {
		var me = this

		var found_list = new Array()

		$.each(frm.doc[tablename], function(idx, row) {
			if (me.has(row[tablename], found_list)) {
				
				frappe.msgprint(__("{0}: El elemento {1} esta duplicado en la fila {2}", 
					[frm.fields_dict[tablename].df.label, row[tablename], row.idx]))

				validated = false
			} else {

				found_list.push(row[tablename])
			}
		})
	},
})