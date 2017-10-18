// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.provide("pws.utils")
frappe.provide("pws.prompt")

frappe.ui.form.on('Proyecto', {
	setup: function(frm) {
		var link_field = "item"
		var fields_dict = {
			"description": "notes",
			"item_name": "item_name"
		}

		$.each(fields_dict, function(source_field, target_field) {
			frm.add_fetch(link_field, source_field, target_field)
		})
	},
	refresh: function(frm) {
		var events = ["add_custom_buttons", "set_queries",
			"set_read_only_table", "set_table_indicators", "set_view_task"]

		$.map(events, function(event) {
			frm.trigger(event)
		})

		frm.$wrapper.find("a.add-attachment").off()
			.on("click", function() {
				frm.trigger("new_attachment")
			})
	},
	onload: function(frm) {
		var events = ["set_read_only_form", "setup_prompt"]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	onload_post_render: function(frm) {
		var has_no_tasks = !! frm.doc.tasks 
			&& !! frm.doc.tasks.length

		if ( ! has_no_tasks) {
			frm.trigger("show_prompt")
		} else if (frm.is_new()) {
			frm.trigger("set_todays_date_as_start_date")
		}

		$(".layout-main .form-column.col-sm-12 > form > .input-max-width").css("min-width", "100%")
	},
	validate: function(frm) {
		if ( ! flt(frm.doc.production_qty)) {
			frappe.throw("¡Cantidad a producir es invalida!")
		}
	},
	production_qty: function(frm) {
		var formatted_qty = flt(frm.doc.production_qty)
			.formatInteger()

		setTimeout(function() {
			frm.doc.production_qty = formatted_qty
			refresh_field("production_qty")
		}, 99)
	},
	set_queries: function(frm) {
		var events = ["set_item_query", "set_sales_order_query"]

		$.map(events, function(event) {
			frm.trigger(event)
		})
	},
	set_read_only_form: function(frm) {
		var is_same_user = (frappe.session.user == frm.doc.owner)
		var is_manager = frappe.user.has_role("Supervisor de Proyectos")

		var fields = [
			"company", "customer",
			"estimated_costing",
			"expected_end_date",
			"gross_margin", "is_active",
			"item", "item_name", "notes",
			"per_gross_margin",
			"percent_complete_method",
			"priority", "production_qty",
			"project_manager", "project_name", 
			"project_type", "status", "title",
			"total_billing_amount", "total_costing_amount",
			"total_expense_claim", "total_purchase_cost",
			"total_sales_cost", "sales_order"
		]

		$.map(fields, function(key) {
			frm.toggle_enable(key, is_same_user || is_manager || frm.is_new())
		})

		if ( ! frm.is_new() && ! is_manager && ! is_same_user) {
			frm.disable_save()
		}
	},
	set_sales_order_query: function(frm) {
		frm.set_query("sales_order", function() {
			return {
				"filters": {
					"docstatus": "1"
				}
			}
		})
	},
	set_view_task: function(frm) {
		var row = frm.body.find("div[data-fieldname=tasks]")
			.find(".grid-row")

		row.each(function(key, html) {
			var $me = $(this)
			var docname = $me.attr("data-name")
			var task_id = frappe.model.get_value("Tarea de Proyecto", docname, "task_id")
				
			if (task_id) {
				$me.off().find("*").off()

				$me.on("click", function(event) {
					if (docname) {

						setTimeout(function() {
							frappe.set_route(["Form", "Tarea", task_id])
						}, 299)
					}

					event.stopPropagation()
				})  
			}
		})
	},
	expected_start_date: function(frm) {
		var fmt = "YYYY-MM-DD HH:mm:ss"
		var m = moment(frm.doc.expected_start_date, fmt)
		var next_month = m.add(1, "months")

		var exp_start_date = frm.doc.expected_start_date

		$.map(frm.doc.tasks, function(row) {
			var m = {
				format: function() {
					return ""
				}
			}

			if (frm.doc.dependant && pws.prev_closed_date) {
				m = moment(pws.prev_closed_date, fmt)
			} else {
				m = moment(exp_start_date, fmt)
			}
			
			row.start_date = m.format(fmt)

			row.end_date = moment(row.start_date, fmt)
				.add(row.max_time, row.time_unit).format(fmt)

			exp_start_date = row.end_date
			
			pws.prev_closed_date = row.closed_date
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
	set_table_indicators: function(frm) {
		var do_for_each = function(idx, html_row) {
			
			var row = frappe.get_doc("Tarea de Proyecto", $(html_row).attr("data-name"))
			var fmt = "YYYY-MM-DD HH:mm:ss"
			
			// exit if not row was found
			if ( ! row) { return ; }

			var status = row.status

			var colors = {
				"Open": "blue",
				"Delayed": "red",
				"Overdue": "red",
				"Working": "blue",
				"Closed": "green",
				"Cancelled": "grey",
				"Pending Review": "blue"
			}

			if (row.dependant) {
				$(html_row).find(".octicon.octicon-triangle-down")
					.removeClass()
					.addClass("octicon octicon-mail-reply")
			}
			
			if (status == "Open" || status == "Pending Review" || status == "Working") {

				var any_pending = false
				if (row.dependant) {

					var dependant_list = (row.depends_on || "").split(", ")

					$.map(dependant_list, function(subject) {
						if ( ! subject) { return ; }

						task = frappe.get_doc("Tarea de Proyecto", { "title": subject })

						if ( ! task) { return ; }

						if (task.status != "Closed") {
							any_pending = true
						}
					})

					if ( ! any_pending && moment().format(fmt) > row.end_date) {
						status = "Delayed"
					} else {
						status = "Open"
						colors["Open"] = "blue"
					}
				} else {
					if (moment().format(fmt) > row.end_date) {
						status = "Delayed"
					}
				}
			}

			$(this).find("[data-fieldname=title]").find(".static-area.ellipsis")
				.find("span").remove()

			$(this).find("[data-fieldname=title]").find(".static-area.ellipsis")
				.prepend(__("<span title=\"{1}\" class=\"indicator {0}\"></span>", 
					[colors[status], status]))
		}

		frm.page.body.find("[data-fieldname=tasks]").find(".grid-body")
			.find(".grid-row").each(do_for_each)

		frm.body.find(".octicon.octicon-triangle-down").hide()
	},
	set_item_query: function(frm) {
		var query = "pws.queries.item_query"

		frm.set_query("item", function() {
			return {
				"query": query
			}
		})
	},
	set_read_only_table: function(frm) {
		var has_permission = frappe.user.has_role("Supervisor de Proyectos")

		if ( ! has_permission) {
			// frm.set_df_property("tasks", "read_only", ! has_permission)

			var fields = ["title", "user", "start_date", "end_date", "description"]

			$.map(fields, function(field) {
				// frm.set_df_property(field, "read_only", ! has_permission, frm.docname, "tasks")
			})
		}
	},
	setup_prompt: function(frm) {
		var fields = {
			"label": "Template", 
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

		pws.prompt.get_field("project_template").get_query = function() {
			return {
				"query": "pws.queries.project_template_query"
			}
		}
	},
	set_todays_date_as_start_date: function(frm) {
		frm.set_value("expected_start_date", 
			frappe.datetime.now_datetime())

		// var fmt = "YYYY-MM-DD HH:mm:ss"
		// var now_datetime = frappe.datetime.now_datetime()
		// var m = moment(now_datetime, fmt)

		// if (frappe.datetime.now_time() < "08:00:00") {
		// 	// let's put it to the 8:00 o'clock
		// 	var today = frappe.datetime.now_date()

		// 	frm.set_value("expected_start_date", today + " 08:00:00")
		// } else if (frappe.datetime.now_time() < "17:00:00") {
		// 	// this is working hours then
		// 	var now_time = m.startOf("hour")
		// 	var an_hour_later = now_time.add(1, "hour")
			
		// 	frm.set_value("expected_start_date", an_hour_later.format(fmt))
		// } else {
		// 	// this must be for tomorrow
		// 	var tomorrow = m.add(1, "days").format("YYYY-MM-DD")

		// 	frm.set_value("expected_start_date", tomorrow + " 08:00:00")
		// }
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
				frappe.show_progress("Subiendo archivo", 2.000, 2.000)

				setTimeout(function() {
					if (response.exec) {
						frappe.msgprint("¡Hubo un problema mientras se cargaba el archivo!")
					} else {
						frm.reload_doc()
					}

					frappe.hide_progress()
				}, 999)
			}

			frappe.show_progress("Subiendo archivo", 1.5, 2.000)
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
		frm.set_value("percent_complete", pws.utils.update_completed(frm))
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

$.extend(pws.utils, {
	update_completed: function(frm) {
		var tasks = frm.doc.tasks.filter(function(row){
			return row.status != "Cancelled";
		})

		var closed_tasks = frm.doc.tasks.filter(function(row){
			return row.status == "Closed";
		})
		
		tasks = tasks.length
		closed_tasks = closed_tasks.length

		return closed_tasks / tasks * 100.000
	}
})
