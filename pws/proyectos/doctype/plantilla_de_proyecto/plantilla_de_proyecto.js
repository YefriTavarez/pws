// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

// frappe.provide("pws.p_template.dependant_tasks")

frappe.ui.form.on('Plantilla de Proyecto', {
	refresh: function(frm) {
		if ( ! frm.is_new()) {
			frm.trigger("add_custom_buttons")
		}

		frm.page.show_menu()
	},
	onload_post_render: function(frm) {
		// pws.p_template.dependant_tasks.init(frm)
	},
	validate: function(frm) {
		frm.trigger("validate_dependant_tasks")
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
				"width": "50%"
			})

		main.find("[data-fieldname=tasks]")
			.find("[data-fieldname=user]").css({
				"width": "33.3333%"
			})
	},
	validate_dependant_tasks: function(frm) {
		if (frm.doc["tasks"] && frm.doc["tasks"][0] && frm.doc["tasks"][0]["dependant"]) {
			frappe.validated = false

			frappe.msgprint({
				"title": "Error de dependencia",
				"message": "¡Tarea #1 no puede depender de ninguna otra!", 
				"indicator": "red"
			})
		}

		$.map(frm.doc.tasks || [], function(row) {
			if (row.dependant && ! row.depends_on) {
				frappe.validated = false

				frappe.msgprint({
					"indicator": "red",
					"title": "Error de dependencia",
					"message": __("¡La Tarea No. {0} fue marcada como dependiente, \
						pero no se le fue especificada ninguna dependencia!", [row.idx])
				})		
			}
		})
	}
})

frappe.ui.form.on("Tarea de Plantilla", {
	"dependant": function(frm, cdt, cdn) {
		// pws.p_template.dependant_tasks.on_dependant(frm, cdt, cdn)
	},
	show_dependency_table: function(frm, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn)

		var dialog = pws.p_template.dependency_table.init(frm, row)
		dialog.show()
	}
})

frappe.provide("pws.p_template.dependency_table")

pws.p_template.dependency_table.current_row = null

$.extend(pws.p_template.dependency_table, {
	init: function(frm, cur_row) {
		this._frm = frm
		this.cur_row = cur_row
		pws.p_template.dependency_table.current_row = cur_row

		this.setup()

		return this.dialog
	},
	show: function() {
		if ( ! this._is_setup) {
			this.init()
		}

		this.dialog.show()
	},
	hide: function() {
		this.dialog.hide()
	},
	setup: function() {
		var me = this
		this.str_rows=  []
		me._is_setup = true

		var string_values = me.cur_row.depends_on
		
		var index = 0
		$.each(string_values? string_values.split(", "): [], function(idx, value) {
			if (value) {
				index += 1

				var datarow = repl(me.template_row, {
					"idx": index,
					"subject": value
				})

				me.str_rows.push(datarow)
			}
		})

		var replaceable_values = ['<div class="rows">', me.str_rows.join("\n"), '</div>']

		var options = repl(me.html_options, {
			"rows_or_nodata": me.str_rows.length? __("{0}{1}{2}", replaceable_values):
				'<div class="grid-empty text-center">No Data</div>'
		})

		$(me.dialog.body).empty()
		$(options).appendTo(me.dialog.body)
			.find(".btn.btn-xs.btn-default.grid-add-row").on("click", function(event) {
				var tasks = frappe.get_list("Tarea de Plantilla")

				var _options = []

				$.map(tasks, function(row) {
					if (row.idx != pws.p_template.dependency_table.current_row.idx) {
						_options.push(row.title)
					}
				})

				var fields = {
					"label": "Task",
					"fieldtype": "Select",
					"fieldname": "task",
					"options": _options.join("\n")
				}

				frappe.prompt(fields, me.add_row_action, "Nueva dependencia", "Agregar")
			})

		$(me.dialog.body).find(".grid-row-check.pull-left").off("change")
			.on("change", function(event) {
				var parent = $(this).parents(".grid-heading-row")

				if (parent.html()) {
					// this is the header check

					var is_checked = $(this).prop("checked")

					$(me.dialog.body).find(".grid-body").find(".grid-row-check.pull-left")
						.prop("checked", is_checked)
				} 

				var all_unchecked = !! $(".grid-row-check.pull-left:checked").length

				if (all_unchecked) {
					$(me.dialog.body).find(".btn.btn-xs.btn-danger.grid-remove-rows")
						.removeClass("hide")
				} else {
					$(me.dialog.body).find(".btn.btn-xs.btn-danger.grid-remove-rows")
						.addClass("hide")
				}
			})

		$(me.dialog.body).find(".btn.btn-xs.btn-danger.grid-remove-rows").on("click", function() {
			$(".grid-row-check.pull-left:checked").each(function(row) {
				var subject = $(this).attr("data-subject")
				var list = pws.p_template.dependency_table.current_row.depends_on.split(", ")

				var set = new Set(list)

				if (set.has(subject)) {
					set.delete(subject)
				}

				var list_updated = Array.from(set)
				pws.p_template.dependency_table.current_row.depends_on = list_updated.join(", ")
			})

			pws.p_template.dependency_table.setup()
		})
	},
	html_options: `<div style="display: flex;" class="section-body">
		<div class="form-column col-sm-12">
			<div class="frappe-control" data-fieldname="dependency_table">
				<div class="form-grid">
					<div class="grid-heading-row">
						<div class="grid-row">
							<div class="data-row row">
								<div class="row-index sortable-handle col col-xs-1">
									<input type="checkbox" class="grid-row-check pull-left">
									<span>&nbsp;</span>
								</div>
								<div class="col grid-static-col col-xs-10  grid-overflow-no-ellipsis" data-fieldname="subject">
									<div class="static-area ellipsis">Subject</div>
								</div>
							</div>
						</div>
					</div>
					<div class="grid-body">
						%(rows_or_nodata)s
						<div class="small form-clickable-section grid-footer">
							<div class="row">
								<div class="col-sm-6 grid-buttons">
									<button type="reset" class="btn btn-xs btn-danger grid-remove-rows hide">Delete</button>
									<button type="reset" class="btn btn-xs btn-default grid-add-row">Add Row</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>`,
	template_row : `<div class="grid-row">
		<div class="data-row row">
			<div class="row-index sortable-handle col col-xs-1">
				<input type="checkbox" data-subject="%(subject)s" class="grid-row-check pull-left">
				<span>%(idx)s</span>
			</div>
			<div class="col grid-static-col col-xs-10  grid-overflow-no-ellipsis" data-fieldname="subject">
				<div class="static-area ellipsis">%(subject)s</div>
			</div>
		</div>
	</div>`,
	dialog: new frappe.ui.Dialog({
		"title": "Tareas dependientes",
		"primary_action_label": "Continuar",
		"primary_action": function(data) {
			pws.p_template.dependency_table.dialog.hide()
		}
	}),
	add_row_action: function(data) {
		if (data) {
			var task = data.task

			var a = (pws.p_template.dependency_table.current_row.depends_on || "").split(", ")

			if (a.length == 1 && a[0] == "") {
				a = []
			}

			a.push(task)

			var unique = Array.from(new Set(a))

			pws.p_template.dependency_table.current_row.depends_on = unique.join(", ")
			pws.p_template.dependency_table.setup()
		}
	},
})
