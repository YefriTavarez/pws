// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.prompt")
frappe.ui.form.on('Proyecto', {
	setup: function(frm) {
		frm.add_fetch("item", "description", "notes")
	},
	refresh: function(frm) {
		var events = ["add_custom_buttons", "set_read_only_table"]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	onload: function(frm) {
		frm.trigger("setup_prompt")
	},
	onload_post_render: function(frm) {
		frm.trigger("show_prompt")

		if (frm.is_new()) {
			frm.trigger("set_todays_date_as_start_date")
		}
	},
	expected_start_date: function(frm) {
		var next_month = frappe.datetime.add_months(frm.doc.expected_start_date, 1)
		frm.set_value("expected_end_date", next_month)
	},
	add_custom_buttons: function(frm) {
		if (frm.is_new()) {
			frm.trigger("add_load_from_template_button")
		}
	},
	add_load_from_template_button: function(frm) {
		frm.add_custom_button("Plantilla de Proyecto", function() {
			frm.trigger("load_from_template")
		}, "Desde")
	},
	load_from_template: function(frm) {
		frm.trigger("show_prompt")
	},
	set_read_only_table: function(frm) {
		var has_permission = frappe.user.has_role("Supervisor de Proyectos")

		if ( !has_permission) {
			frm.set_df_property("tasks", "read_only", !has_permission)

			var fields = ["title", "user", "start_date", "end_date", "task_weight", "description"]

			$.map(fields, function(field) {
				frm.set_df_property(field, "read_only", !has_permission, frm.docname, "tasks")
			})
		}
	},
	setup_prompt: function(frm) {
		var fields = {
			"label":"Template", 
			"fieldname": "project_template", 
			"fieldtype": "Link", 
			"options": "Plantilla de Proyecto"
		}

		pws.prompt = new frappe.ui.Dialog({
			title: "Template del cual se cargara la informacion",
			fields: [fields],
			onhide: function() {
				frm.$wrapper.show()
			}
		})
	},
	set_todays_date_as_start_date: function(frm) {
		frm.set_value("expected_start_date", frappe.datetime.get_today())
	},
	show_prompt: function(frm) {
		if ( !!(frm.doc.tasks || []).length) {
			return // do not continue, as the user has already chose the template
		}

		// provide with namespace flags
		frappe.provide("pws.flags")

		var primary_label = "Cargar"
		
		if (frm.is_new()) {

			frm.$wrapper.hide()

			pws.prompt.set_primary_action(primary_label, function() {
				var data = pws.prompt.get_values()
				
				if (data) {
					frm.doc.plantilla_de_proyecto  = data.project_template

					frm.call("create_project", "args", function(response) {
						frm.refresh()
					})

					pws.prompt.hide()
				}

				// set the flag in order to clear the field next time it will open
				pws.flags.first_completed = true
			})

			// clear the field if the first_completed flag is set
			pws.flags.first_completed && pws.prompt.get_field("project_template").$input.val("")
			pws.prompt.show()
		}
	}
})

frappe.ui.form.on("Tarea de Proyecto", {
	status: function(frm, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn)
		var username = frappe.user.name

		var has_permission = frappe.user.has_role("Supervisor de Proyectos")
		if ( ! (has_permission || row.user == username)) {
			frm.reload_doc()

			frappe.throw("¡No puede actualizar el estado de la tarea de otro usuario!")
		}
	}
})
