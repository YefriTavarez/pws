// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tecnologia de Impresion', {
	"refresh": (frm) => {
		frm.trigger("add_custom_buttons");
	},
	"add_custom_buttons": (frm) => {
		if (frm.doc.enabled) {
			frm.add_custom_button("Deshabilitar", () => frm.trigger("disable"));
		} else {
			frm.add_custom_button("Habilitar", () => frm.trigger("enable"));
		}
	},
	"enable": (frm) => {
		frappe.run_serially([
			() => frm.set_value("enabled", true),
			() => frm.save()
		]);
	},
	"disable": (frm) => {
		frappe.run_serially([
			() => frm.set_value("enabled", false),
			() => frm.save()
		]);
	}
});
