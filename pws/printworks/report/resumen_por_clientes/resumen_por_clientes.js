// Copyright (c) 2016, Yefri Tavarez and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Resumen por Clientes"] = {
	"filters": [
		{
			"label": __("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_default("company"),
			"reqd": 1,
		},
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"reqd": 1,
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
			"reqd": 1,
		},
		{
			"label": __("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer"
		},
	]
}
