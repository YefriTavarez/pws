// Copyright (c) 2016, Yefri Tavarez and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Promedio por Tareas"] = {
	"filters": [
		{
			"label": "Desde Fecha",
			"fieldname": "from_date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.month_start()
		},
		{
			"label": "Hasta Fecha",
			"fieldname": "to_date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.month_end()
		},
		{
			"label": "Tarea",
			"fieldtype": "Select",
			"fieldname": "task",
			// "reqd": 1,
			"options": frappe.boot.task_list
		}
	]
};
