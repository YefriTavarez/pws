// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tarea', {
	refresh: function(frm) {
		var is_same_user = (frappe.session.user == frm.doc.user)
		var is_manager = frappe.user.has_role("Supervisor de Proyectos")

		if ( ! is_same_user && ! is_manager) {
			// frappe.show_not_permitted("Error de permisos")

			frm.trigger("set_as_read_only_fields")
		}
	},
	onload: function(frm) {
		frm.doc.previous_status = frm.doc.status
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
	set_as_read_only_fields: function(frm) {
		var fields = [
			"actual_time",
			"close_date",
			"company",
			"dependant",
			"depends_on",
			"exp_end_date",
			"exp_start_date",
			"expected_time",
			"priority",
			"project",
			"project_name",
			"status",
			"subject",
			"description"
		]

		$.map(fields, function(field) {
			frm.toggle_enable(field, false)
		})

		frm.disable_save()
	},
	status: function(frm) {
		if (frm.doc.status == "Open" && frm.doc.previous_status == "Overdue") {
			frm.set_value("status", frm.doc.previous_status)
			frappe.throw("¡No puede cambiar el estado de la Tarea a Abierto porque ya esta Atrasada!")
		}

		if (frm.doc.status == "Closed" || frm.doc.status == "Cancelled") {
			// ToDo: tell the server that this task was closed

			frm.doc.close_date = frappe.datetime.now_datetime()
		}
	}
})
