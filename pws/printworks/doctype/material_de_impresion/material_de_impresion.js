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
	},
	validate: function(frm) {
		// frappe.dom.freeze("Espere...")

		var method = "pws.printworks.doctype.material_de_impresion.material_de_impresion.rename_doc"

		var args = { 
			"frm_doc": frm.doc 
		}

		var callback = function(response) {
			var new_name = response.message

			if (new_name) {
				frappe.set_route(["Form", "Material de Impresion", new_name])
				// frappe.dom.unfreeze()
			}
		}

		var error = function(response) {
			// frappe.dom.unfreeze()
		}
		
		setTimeout(function() {

			frappe.call({ "method": method, "args": args, "callback": callback, "error": error })
		})
	}
})
