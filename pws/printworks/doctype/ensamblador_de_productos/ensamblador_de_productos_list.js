// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.utils")

frappe.listview_settings["Ensamblador de Productos"] = {
	add_fields: [

	],
	onload: function(listview) {
		listview.add_button("Ver Detalle", function() {
			$.each(listview.get_checked_items(), function(idx, value) {
				pws.utils.show_assembler_details(value)
			})
		})
	},
	refresh: function(listview) {
		var list = listview.data

		setTimeout(function() {

			$(".avatar.avatar-small.avatar-empty").each(function(idx, row) {
				$(this).text("Mas").on("click", function(event) {
					// var row = listview.data[]
					event.stopPropagation()
				}).on("mouseover", function(event) {
					$(this).text("[Mas]")
				}).on("mouseout", function(event) {
					$(this).text("Mas")
				})
			})
		},999)
	}
}

$.extend(pws.utils, {
	"show_assembler_details": function(body) {
		var _body = body["name"]? "<h1>Codigo: <a href='/desk#Form/Ensamblador de Productos/%(name)s'>%(name)s</a></h1>": ""

		_body += body["perfilador_de_productos"]? "<b>Perfilador:</b> %(perfilador_de_productos)s<br>": ""
		_body += body["dimension"]? "<b>Dimension:</b> %(dimension)s<br>": ""
		_body += body["material_nombre"]? "<b>Material:</b> %(material_nombre)s<br>": ""
		_body += body["material_calibre"]? "<b>Calibre:</b> %(material_calibre)s<br>": ""
		_body += body["material_caras"]? "<b>Material Caras:</b> %(material_caras)s<br>": ""
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
