# Copyright (c) 2013, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe import _

def execute(filters=None):
	return get_columns(filters), get_data(filters)

def get_columns(filters=None):
	return [
		{
			"label": _("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": 180,
		},
		{
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 300,
		},
		# {
		# 	"label": _("Customer Name"),
		# 	"fieldtype": "Data",
		# 	"width": 250,
		# },
		{
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100,
		},
		{
			"label": _("Pending Amount"),
			"fieldtype": "Float",
			"default": 0.000,
			"width": 120,
		},
		{
			"label": _("Paid Amount"),
			"fieldtype": "Float",
			"default": 0.000,
			"width": 120,
		},
		{
			"label": _("Total Amount"),
			"fieldtype": "Float",
			"default": 0.000,
			"width": 120,
		},
	]
def get_data(filters=None):
	return frappe.db.sql("""
		SELECT
			company,
			customer,
			# customer_name,
			currency,
			SUM(outstanding_amount) pending,
			SUM(grand_total - outstanding_amount) paid,
			SUM(grand_total) total 
		FROM
			`tabSales Invoice` 
		WHERE
			%(filters)s
		GROUP BY
			customer,
			currency 
		ORDER BY
			customer
	""" % { "filters": get_conditions(filters) }, filters, as_list=True, debug=True)

def get_conditions(filters=None):
	conditions = []

	if filters.get("customer"):
		conditions.append("customer = %(customer)s")
	
	conditions.append("posting_date BETWEEN %(from_date)s AND %(to_date)s")

	return " AND ".join(conditions)