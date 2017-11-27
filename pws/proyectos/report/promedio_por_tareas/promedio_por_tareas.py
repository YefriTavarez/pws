# Copyright (c) 2013, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	return get_columns(filters), get_data(filters)

def get_columns(filters):
	return [
		"Tarea:Data:300",
		"Tiempo Promedio:Time:200",
	]

def get_data(filters):
	result = frappe.db.sql("""SELECT
			subject,
			SEC_TO_TIME(AVG(TIME_TO_SEC(TIMEDIFF(exp_end_date, exp_start_date))))
		FROM
			tabTarea 
		WHERE
			%(filters)s
		GROUP BY subject
		ORDER BY idx""" % { 
			"filters": get_filters(filters)
		}, filters, as_dict=False)

	return result

def get_filters(filters):
	queries = ["1=1"]

	if filters.get("from_date"):
		queries.append("creation >= %(from_date)s")

	if filters.get("to_date"):
		queries.append("creation <= %(to_date)s")

	if filters.get("task"):
		queries.append("subject = %(task)s")

	return " AND ".join(reversed(queries))

