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
		frm.trigger("toggle_color_fields");
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
	toggle_color_fields: function(frm) {
		const colors_for_sku = frm.doc.__onload.colors_for_sku;

		if (!colors_for_sku) { return ; }
		if (!frm.doc.enable_colors) { return ; }

		const color_fields = [
			"color_pantone_tiro_1",
			"color_pantone_tiro_2",
			"color_pantone_tiro_3",
			"color_pantone_tiro_4",

			"color_pantone_retiro_1",
			"color_pantone_retiro_2",
			"color_pantone_retiro_3",
			"color_pantone_retiro_4",

			"color_proceso_tiro_1",
			"color_proceso_tiro_2",
			"color_proceso_tiro_3",
			"color_proceso_tiro_4",

			"color_proceso_retiro_1",
			"color_proceso_retiro_2",
			"color_proceso_retiro_3",
			"color_proceso_retiro_4",
		];

		$.map(color_fields, function(field) {
			frm.toggle_display(field, false);
		});

		for (index = 1; index <= cint(colors_for_sku.cantidad_tiro_pantone); index ++) {
			const fieldlist = [	
				"color_pantone_tiro_1",
				"color_pantone_tiro_2",
				"color_pantone_tiro_3",
				"color_pantone_tiro_4",
			];

			frm.toggle_display(fieldlist[index - 1], true);
		}

		for (index = 1; index <= cint(colors_for_sku.cantidad_pantone_retiro); index ++) {
			const fieldlist = [	
				"color_pantone_retiro_1",
				"color_pantone_retiro_2",
				"color_pantone_retiro_3",
				"color_pantone_retiro_4",
			];
			frm.toggle_display(fieldlist[index - 1], true);
		}

		for (index = 1; index <= cint(colors_for_sku.cantidad_tiro_proceso); index ++) {
			const fieldlist = [	
				"color_proceso_tiro_1",
				"color_proceso_tiro_2",
				"color_proceso_tiro_3",
				"color_proceso_tiro_4",
			];
			
			frm.toggle_display(fieldlist[index - 1], true);
		}

		for (index = 1; index <= cint(colors_for_sku.cantidad_proceso_retiro); index ++) {
			const fieldlist = [	
				"color_proceso_retiro_1",
				"color_proceso_retiro_2",
				"color_proceso_retiro_3",
				"color_proceso_retiro_4",
			];
			
			frm.toggle_display(fieldlist[index - 1], true);
		}
	},
	status: function(frm) {
		if (frm.doc.status == "Open" && frm.doc.previous_status == "Overdue") {
			if (frm.doc.exp_end_date < frappe.datetime.now_datetime()) {
				frm.set_value("status", frm.doc.previous_status)
				frappe.throw("¡No puede cambiar el estado de la Tarea a Abierto porque ya esta Atrasada!")
			}
		}

		if (frm.doc.status == "Closed") {
			frm.doc.was_closed = true
			frm.doc.close_date = frappe.datetime.now_datetime()
		}
	}
})
