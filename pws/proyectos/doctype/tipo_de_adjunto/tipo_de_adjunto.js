// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tipo de Adjunto', {
	refresh: function(frm) {

	},
	attach_type: function(frm) {
		var abbr = frappe.get_abbr(frm.doc.attach_type)
		frm.set_value_if_missing("abbr", abbr.toUpperCase())
	}
})
