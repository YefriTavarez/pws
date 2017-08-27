// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.utils")

frappe.listview_settings["Ensamblador de Productos"] = {
	add_fields: [
		"opciones_de_textura",
		"cantidad_tiro_proceso",
		"cantidad_proceso_retiro",
		"cantidad_tiro_pantone",
		"cantidad_pantone_retiro",
	],
	onload: function(listview) {
		listview.add_button("Ver Detalle", function() {
			$.each(listview.get_checked_items(), function(idx, value) {
				pws.utils.show_assembler_details(value)
			})
		})
	},
	post_render_item: function(listview, html_row, value) {

		frappe.call({
			"method": "frappe.client.get_list",
			"args": {
				"doctype": "Opciones de Textura Items",
				"fields": [
					"idx",
					"opciones_de_textura"
				],
				"filters": {
					"parent": value.name
				},
				"limit_page_length": "0",
				"order_by": "idx"
			},
			"callback": function(response) {
				var textura_list = response.message

				if (textura_list) {
					$.each(textura_list, function(idx, row) {
						value.opciones_de_textura += repl(
							"<br><span style='margin-left: 10px;'>%(idx)s - %(opciones_de_textura)s</span>",
							row
						)
					})
				}
			}
		})

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
		var _body = body["name"]? "<h1><a href='/desk#Form/Ensamblador de Productos/%(name)s'>%(name)s</a></h1>": ""

		_body += body["perfilador_de_productos"]? "<b>Perfilador:</b> %(perfilador_de_productos)s<br>": ""
		_body += body["dimension"]? "<b>Dimension:</b> %(dimension)s<br>": ""
		_body += body["material_nombre"]? "<b>Material:</b> %(material_nombre)s<br>": ""
		_body += body["material_calibre"]? "<b>Calibre:</b> %(material_calibre)s<br>": ""
		_body += body["material_caras"]? "<b>Material Caras:</b> %(material_caras)s<br>": ""
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
	}
})
