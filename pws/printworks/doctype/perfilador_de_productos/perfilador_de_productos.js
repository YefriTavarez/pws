// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.utils")

frappe.ui.form.on('Perfilador de Productos', {
	refresh: function(frm) {
		if ( !frm.is_new()) {
			frm.trigger("add_buttons"), frm.trigger("re_tiro")
		}

		frm.trigger("tiene_respaldo")
	},
	onload_post_render: function(frm) {
		if (frm.is_new()) {
			frm.trigger("clear_and_fill_tables")			
		}
	},
	validate: function(frm) {
		frm.trigger("validate_duplicates")
	},
	add_buttons: function(frm) {
		frm.add_custom_button("Reset Form", function(event) {
			frm.trigger("reset_form")
		})
	},
	reset_form: function(frm) {
		frm.trigger("clear_and_fill_tables")
	},
	re_tiro: function(frm) {
		frm.set_value("tiro", true) 
		frm.set_df_property("tiro", "read_only", !!frm.doc.re_tiro)
	},
	tiene_respaldo: function(frm) {
		pws.utils.set_respaldo_materiales(frm)
		frm.set_df_property("respaldo_sb", "hidden", !frm.doc.tiene_respaldo)
	},
	validate_duplicates: function(frm) {
		var tables = [
			"materials",
			"opciones_de_control",
			"opciones_de_corte",
			"opciones_de_empalme",
			"opciones_de_proteccion",
			"opciones_de_plegado",
			"opciones_de_utilidad",
			"opciones_de_textura"
		]

		$.each(tables, function(idx, tablename) {
			pws.utils.validate_table(frm, tablename)
		})
	},
	clear_and_fill_tables: function(frm) {
		var triggers = [
			"fill_tabla_materiales",
			"fill_tabla_opciones_de_control",
			"fill_tabla_opciones_de_corte",
			"fill_tabla_opciones_de_empalme",
			"fill_tabla_opciones_de_proteccion",
			"fill_tabla_opciones_de_plegado",
			"fill_tabla_opciones_de_utilidad",
			"fill_tabla_opciones_de_textura"
		]

		$.each(triggers, function(idx, trigger) {
			frm.trigger(trigger)
		})
	},
	fill_tabla_materiales: function(frm) {

		pws.utils.fill_table(frm, "Material de Impresion", "materials", "materials")
	},
	fill_tabla_opciones_de_control: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Control", "opciones_de_control", "opciones_de_control")
	},
	fill_tabla_opciones_de_corte: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Corte", "opciones_de_corte", "opciones_de_corte")
	},
	fill_tabla_opciones_de_empalme: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Empalme", "opciones_de_empalme", "opciones_de_empalme")
	},
	fill_tabla_opciones_de_proteccion: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Proteccion", "opciones_de_proteccion", "opciones_de_proteccion")
	},
	fill_tabla_opciones_de_plegado: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Plegado", "opciones_de_plegado", "opciones_de_plegado")
	},
	fill_tabla_opciones_de_utilidad: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Utilidad", "opciones_de_utilidad", "opciones_de_utilidad")
	},
	fill_tabla_opciones_de_textura: function(frm) {

		pws.utils.fill_table(frm, "Opciones de Textura", "opciones_de_textura", "opciones_de_textura")
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
	"fill_table": function(frm, child_doctype, child_fieldname, fieldname, respaldo=undefined) {
		frm.doc[child_fieldname] = new Array()

		var method = "frappe.client.get_list"

		var args = {
			"doctype": child_doctype,
			"fields": ["name"],
			"filters": {
				"enabled": "1"
			},
			"limit_page_length": 0
		}

		if (respaldo) {
			$.extend(args, {
				"filters": {
					"enabled": "1",
					"es_respaldo": "1"
				}
			})
		}

		var callback = function(response) {
			var list = response.message

			if (list) {
				$.each(list, function(idx, value) {
					child = frm.add_child(child_fieldname)

					child[fieldname] = value.name
				})

				frm.refresh_fields()
			}
		}

		frappe.call({ "method": method, "args": args, "callback": callback })
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
	set_respaldo_materiales: function(frm) {
		var me = this

		if (frm.doc.tiene_respaldo) {

			me.fill_table(frm, "Material de Impresion", "respaldo_materiales", "materials", true)
		} else {

			frm.set_value("respaldo_materiales", new Array())
		}
	}
})