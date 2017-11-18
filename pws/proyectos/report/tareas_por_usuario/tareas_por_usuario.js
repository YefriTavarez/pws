// Copyright (c) 2016, Yefri Tavarez and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tareas por usuario"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"reqd": "1",
			"default": frappe.datetime.month_start(),
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"reqd": "1",
			"default": frappe.datetime.month_end(),
		},
		{
			"label": __("User"),
			"fieldname": "user",
			"fieldtype": "Link",
			"options": "User",
			"reqd": "1",
			"get_query": function() {
				return {
					"query": "pws.queries.tarea_por_usuario_report_query"
				}
			}
		},
		{
			"label": __("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Proyecto",
		},
	]
}
