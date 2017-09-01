// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.prompt")
frappe.ui.form.on('Proyecto', {
	setup: function(frm) {

		var link_field = "item"
		var fields_dict = {
			"description": "notes",
			 "item_group": "item_name"
		}

		$.each(fields_dict, function(source_field, target_field) {
			frm.add_fetch(link_field, source_field, target_field)
		})
	},
	refresh: function(frm) {
		var events = ["add_custom_buttons", 
			"set_read_only_table", "set_table_indicators"]

		$.map(events, function(event) {
			frm.trigger(event)
		})

		frm.$wrapper.find("a.add-attachment").off()
			.on("click", function() {
				frm.trigger("new_attachment")
			})
	},
	onload: function(frm) {
		frm.trigger("setup_prompt")
	},
	onload_post_render: function(frm) {
		if ( !(frm.doc.tasks || []).length) {
			frm.trigger("show_prompt")
		} else if (frm.is_new()) {
			frm.trigger("set_todays_date_as_start_date")
		}
	},
	expected_start_date: function(frm) {
		var next_month = frappe.datetime.add_months(frm.doc.expected_start_date, 1)
		var exp_start_date = frm.doc.expected_start_date

		$.map(frm.doc.tasks, function(row) {
			row.start_date = moment(exp_start_date + " 08:00:00", "YYYY-MM-DD hh:mm:ss")
				.format("YYYY-MM-DD hh:mm:ss")

			row.end_date = moment(row.start_date, "YYYY-MM-DD hh:mm:ss")
				.add(row.max_time, row.time_unit)
				.format("YYYY-MM-DD hh:mm:ss")
		})

		frm.set_value("expected_end_date", next_month)
		refresh_field("tasks")
	},
	expected_end_date: function(frm) {
		// to do
	},
	add_custom_buttons: function(frm) {
		if (frm.is_new()) {
			frm.trigger("add_load_from_template_button")
		} else {
			// frm.trigger("add_new_attachments_button")
		}
	},
	add_load_from_template_button: function(frm) {
		frm.add_custom_button("Plantilla de Proyecto", function() {
			frm.trigger("load_from_template")
		}, "Desde")
	},
	add_new_attachments_button: function(frm) {
		frm.add_custom_button("Nuevo Adjunto", function() {
			frm.trigger("new_attachment")
		})
	},
	load_from_template: function(frm) {
		frm.trigger("show_prompt")
	},
	set_table_indicators: function(frm) {
		frm.page.body.find("[data-fieldname=tasks]")
			
			.find(".grid-body")

			.find(".grid-row")

			.each(function(idx, html_row) {
				var row = frappe.get_doc("Tarea de Proyecto", $(html_row).attr("data-name"))

				if (row) {
					var colors = {
						"Closed": "green",
						"Open": "orange",
						"Pending Review": "yellow",
						"Working": "blue",
						"Cancelled": "grey",
						"Delayed": "red"
					}

					var status = row.status
					if (status == "Open" || status == "Pending Review" || status == "Working") {
						if (moment().format("YYYY-MM-DD hh:mm:ss") > row.end_date) {
							status = "Delayed"
						}
					}

					$(this).find("[data-fieldname=title]")
						.find(".static-area.ellipsis")
					.find("span").remove()

					$(this).find("[data-fieldname=title]")
						.find(".static-area.ellipsis")
					.prepend(__("<span title=\"{1}\" class=\"indicator {0}\"></span>", 
						[colors[status], status]))
				}
			})
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
						frm.trigger("set_todays_date_as_start_date")
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
	}, 
	new_attachment: function(frm) {
		frappe.provide("pws.ui.current_dialog")

		var dialog = pws.ui.get_upload_dialog({
			"customer": frm.doc.customer,
			"project_name": frm.doc.project_name,
			"item_name": frm.doc.item_name,
			"production_qty": frm.doc.production_qty
		})
	
		var btn = dialog.set_primary_action(__("Adjuntar"), function() {
			var filedata = $('#select_files').prop('filedata')
			var server_module_name = frappe.model.get_server_module_name(frm.doctype)
			var method = __("{0}.attach_file", [server_module_name])

			if ( ! filedata) {
				frappe.throw("¡Debe seleccionar al menos un archivo!")
			}

			var args = {
				"filedata": filedata,
				"doctype": frm.doctype,
				"docname": frm.docname
			}

			var callback = function(response) {
				frappe.show_progress("Subiendo archivo", 2, 2)

				setTimeout(function() {
					if (response.exec) {
						frappe.msgprint("¡Hubo un problema mientras se cargaba el archivo!")
					} else {
						frm.reload_doc()
					}

					frappe.hide_progress()
				}, 999)
			}

			frappe.show_progress("Subiendo archivo", 1.5, 2)
			frappe.call({ "method": method, "args": args, "callback": callback })
			
			dialog.hide()
		})

		pws.ui.current_dialog = dialog
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

		frm.trigger("set_table_indicators")
	},
	edit_task: function(frm, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn)

		frappe.set_route(["Form", "Tarea", row.task_id])
	},
	tasks_add: function(frm, cdt, cdn) {
		frm.trigger("set_table_indicators")
	},
	tasks_move: function(frm, cdt, cdn) {
		setTimeout(function() { 
			frm.trigger("set_table_indicators") 
		}, 99)
	},
	tasks_remove: function(frm, cdt, cdn) {
		setTimeout(function() { 
			frm.trigger("set_table_indicators") 
		}, 150)
	}
})
