// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tarea', {
	refresh: function(frm) {
		var is_same_user = (frappe.session.user == frm.doc.user)
		var is_manager = frappe.user.has_role("Supervisor de Proyectos")

		if ( ! is_same_user && ! is_manager) {
			frappe.show_not_permitted("Error de permisos")
		}
	},
	onload_post_render: function(frm) {
		frappe.provide(__("pws.{0}.tasks_dict", [frm.docname]))

		$.map(frm.doc.depends_on, function(row) {
			var _filters = { 
				"name": row.task
			}
			
			var _callback = function(data) {
				pws[frm.docname].tasks_dict[row.task] = data.status
			}

			frappe.model.get_value("Tarea", _filters, ["status"], _callback)
		})
	},
	status: function(frm) {
		if (frm.doc.status == "Closed" || frm.doc.status == "Cancelled") {
			frm.doc.close_date = frappe.datetime.now_datetime()
		}
	}
})
