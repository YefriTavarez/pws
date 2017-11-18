// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tipo de Adjunto', {
	refresh: function(frm) {
		frm.page.show_menu()
	},
	validate: function(frm) {
		if (frm.doc.allow_more_than_one && frm.doc.max_attacthments == 1) {
			frappe.throw("¡Máximo de adjuntos permitidos no deberia ser uno!")
		} 
	},
	attach_type: function(frm) {
		var abbr = frappe.get_abbr(frm.doc.attach_type)
		frm.set_value_if_missing("abbr", abbr.toUpperCase())
	},
	allow_more_than_one: function(frm) {
		frm.set_value("max_attacthments", 0.000)
	}
})
