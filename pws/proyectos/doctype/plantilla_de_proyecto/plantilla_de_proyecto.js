// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Plantilla de Proyecto', {
	refresh: function(frm) {
		if ( !frm.is_new()) {
			frm.trigger("add_custom_buttons")
		}

		frm.page.show_menu()
	},
	onload_post_render: function(frm) {
		frm.trigger("fix_table_layout")
	},
	add_custom_buttons: function(frm) {
		var events = ["add_create_project_button"]

		$.each(events, function(idx, event) {
			frm.trigger(event)
		})
	},
	add_create_project_button: function(frm) {
		frm.add_custom_button("Crear Proyecto", function() {
			frm.trigger("create_project")
		})
	},
	create_project: function(frm) {
		var callback = function(response) {
			var new_project = response.message

			if (new_project) {
				doc = frappe.model.sync(new_project)[0]
				frappe.set_route("Form", "Proyecto", doc.name)
			} else {
				frappe.msgprint("No se pudo crear el proyecto")
			}
		}

		frm.call("create_project", "args", callback)
	},
	fix_table_layout: function(frm) {
		var main = frm.page.main

		main.find("[data-fieldname=tasks]")
			.find("[data-fieldname=status]").hide()

		main.find("[data-fieldname=tasks]")
			.find("[data-fieldname=start_date]").hide()

		main.find("[data-fieldname=tasks]")
			.find("[data-fieldname=end_date]").hide()

		main.find("[data-fieldname=tasks]")
			.find("[data-fieldname=title]").css({
				"width": "60%"
			})

		main.find("[data-fieldname=tasks]")
			.find("[data-fieldname=user]").css({
				"width": "20%"
			})
	}
})
