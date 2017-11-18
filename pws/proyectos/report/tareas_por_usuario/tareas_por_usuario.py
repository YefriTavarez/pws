# Copyright (c) 2013, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	# columns, data = [], []

	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	return [
		"Tarea:Link/Tarea:100",
		"Titulo:Read Only:300",
		"Retraso:Time:110",
		"Fecha de Creacion:Datetime:160",
		"Fecha de Finalizacion:Datetime:160",
		"Fecha de Cierre:Datetime:160",
		"Estado:Read Only:80",
		"Proyecto:Link/Proyecto:100",
	]

def get_data(filters):
	result = frappe.db.sql("""SELECT
			name, 
			subject, 
			GREATEST(TIMEDIFF(close_date, exp_end_date), "0:00:00"),
			exp_start_date,
			exp_end_date,
			close_date,
			status,
			project 
		FROM `tabTarea`
		WHERE %s
	""" % get_filters(filters), filters, 
	as_dict=False)

	return result
	
def get_filters(filters):
	query = ["status = 'Closed'"]

	filters.get("from_date") and query.append("AND creation >= %(from_date)s")
	filters.get("to_date") and query.append("AND creation <= %(to_date)s")
	filters.get("project") and query.append("AND project = %(project)s")
	filters.get("user") and query.append("AND owner = %(user)s")

	return " ".join(query)


