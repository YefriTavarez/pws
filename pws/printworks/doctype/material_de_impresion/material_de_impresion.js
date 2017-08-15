// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material de Impresion', {
	refresh: function(frm) {
		frm.trigger("add_custom_buttons")
	},
	add_custom_buttons: function(frm) {
		if ( !frm.is_new()) {
			frm.add_custom_button("Duplicar", function(event) {
				frm.copy_doc()
			})
		}
	}
})
