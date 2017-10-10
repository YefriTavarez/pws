// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.utils")

frappe.listview_settings["Ensamblador de Productos"] = {
	add_fields: [
		"cantidad_tiro_proceso",
		"cantidad_proceso_retiro",
		"cantidad_tiro_pantone",
		"cantidad_pantone_retiro",
		"materials_title",
	],
	onload: function(listview) {
		listview.add_button("Ver Detalle", function() {
			$.each(listview.get_checked_items(), function(idx, value) {
				pws.utils.show_assembler_details(value)
			})
		})
	},
	post_render_item: function(listview, html_row, value) {

		var callback = function(response, fieldname) {
			var list = response.message

			value[fieldname] = ""
			
			if (list) {
				$.each(list, function(idx, row) {
					value[fieldname] += repl("<br><span style='margin-left: 10px;'>%(idx)s - %(opts)s</span>", 
						{ "opts": row[fieldname], "idx": row["idx"] })
				})
			}
		}
		
		pws.utils.get_table("Opciones de Proteccion Items", "opciones_de_proteccion", value, callback)
		pws.utils.get_table("Opciones de Textura Items", "opciones_de_textura", value, callback)
		pws.utils.get_table("Opciones de Utilidad Items", "opciones_de_utilidad", value, callback)

		html_row.find(".avatar.avatar-small").text("Ver")
			.on("click", function(event) {
				pws.utils.show_assembler_details(value)
					event.stopPropagation()
		}).on("mouseover", function(event) {
			$(this).css("text-decoration", "underline");
		}).on("mouseout", function(event) {
			$(this).css("text-decoration", "none");
		}).css({"border": "none", "height": "18px"}).find("*").remove()
	}
}

$.extend(pws.utils, {
	"show_assembler_details": function(body) {
		var _body = body["name"]? 
			"<h1 style='margin-top: -5px;'><a href='/desk#Form/Ensamblador de Productos/%(name)s'>%(name)s</a></h1>": ""

		_body += body["perfilador_de_productos"]? "<b>Producto:</b> %(perfilador_de_productos)s<br>": ""
		_body += body["dimension"]? "<b>Dimension:</b> %(dimension)s<br>": ""
		_body += body["materials_title"]? "<b>Material:</b> %(materials_title)s<br>": ""
		_body += flt(body["cantidad_tiro_proceso"])? "<b>Colores Proceso Tiro:</b> %(cantidad_tiro_proceso)s<br>": ""
		_body += flt(body["cantidad_tiro_pantone"])? "<b>Colores Pantone Re-tiro:</b> %(cantidad_tiro_pantone)s<br>": ""
		_body += flt(body["cantidad_proceso_retiro"])? "<b>Colores Proceso Re-tiro:</b> %(cantidad_proceso_retiro)s<br>": ""
		_body += flt(body["cantidad_pantone_retiro"])? "<b>Colores Pantone Tiro:</b> %(cantidad_pantone_retiro)s<br>": ""
		_body += body["opciones_de_control"]? "<b>Opciones de Control:</b> %(opciones_de_control)s<br>": ""
		_body += body["opciones_de_corte"]? "<b>Opciones de Corte:</b> %(opciones_de_corte)s<br>": ""
		_body += body["opciones_de_empalme"]? "<b>Opciones de Empalme:</b> %(opciones_de_empalme)s<br>": ""
		_body += body["opciones_de_plegado"]? "<b>Opciones de Plegado:</b> %(opciones_de_plegado)s<br>": ""
		_body += body["opciones_de_proteccion"]? "<b>Opciones de Proteccion:</b> %(opciones_de_proteccion)s<br>": ""
		_body += body["opciones_de_textura"]? "<b>Opciones de Textura:</b> %(opciones_de_textura)s<br>": ""
		_body += body["opciones_de_utilidad"]? "<b>Opciones de Utilidad:</b> %(opciones_de_utilidad)s<br>": ""

		frappe.msgprint(repl(_body, body))
	},
	"get_table": function(doctype, fieldname, row, original_callback) {
		var method = "frappe.client.get_list"

		var args = {
			"doctype": doctype,
			"fields": ["idx", fieldname],
			"filters": {
				"parent": row["name"]
			},
			"limit_page_length": "0",
			"order_by": "idx"
		}

		var callback = function(response) {
			original_callback && original_callback(response, fieldname)
		}

		frappe.call({ "method": method, "args": args, "callback": callback })
	}
})
