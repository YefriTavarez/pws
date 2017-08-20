// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws")

frappe.ui.form.on('Ensamblador de Productos', {
	refresh: function(frm) {
		frm.trigger("set_queries")
	},
	onload_post_render: function(frm) {
		frm.trigger("perfilador_de_productos")
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
			"set_dimension_query"
		]

		$.each(events, function(idx, event) {
			frm.trigger(event)
		})
	},
	perfilador_de_productos: function(frm) {
		if (frm.doc.perfilador_de_productos) {
			frm.trigger("fetch_the_profile_maker")
		}
	},
	set_material_query: function(frm) {
		frm.set_query("materials", function() {
			var query = "pws.api.ens_materials_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_control_query: function(frm) {
		frm.set_query("opciones_de_control", function() {
			var query = "pws.api.ens_control_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_corte_query: function(frm) {
		frm.set_query("opciones_de_corte", function() {
			var query = "pws.api.ens_corte_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_empalme_query: function(frm) {
		frm.set_query("opciones_de_empalme", function() {
			var query = "pws.api.ens_empalme_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_plegado_query: function(frm) {
		frm.set_query("opciones_de_plegado", function() {
			var query = "pws.api.ens_plegado_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_proteccion_query: function(frm) {
		frm.set_query("opciones_de_proteccion", function() {
			var query = "pws.api.ens_proteccion_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_utilidad_query: function(frm) {
		frm.set_query("opciones_de_utilidad", function() {
			var query = "pws.api.ens_utilidad_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_textura_query: function(frm) {
		frm.set_query("opciones_de_textura", function() {
			var query = "pws.api.ens_textura_query"
			var filters = {
				"perfilador": frm.doc.perfilador_de_productos
			}

			return { "query": query, "filters": filters }
		})
	},
	set_dimension_query: function(frm) {
		frm.set_query("dimension", function() {
			var filters = {
				"product_type": frm.doc.perfilador_de_productos
			}

			return { "filters": filters }
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
	}
})
