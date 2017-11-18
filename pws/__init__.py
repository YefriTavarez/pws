# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.0.1'

@frappe.whitelist()
def rename_doc(doctype, name, force=True):
	doc = frappe.get_doc(doctype, name)
	new_name = doc.make_new_name()

	if not new_name == doc.name:

		return frappe.rename_doc(doc.doctype, 
			doc.name, new_name, force=True)


@frappe.whitelist()
def get_task_status_list(task):
	return frappe.db.sql("""SELECT
			task.status AS status
		FROM
			`tabTarea` AS parent 
			JOIN
				`tabTarea Dependiente de` AS child 
				ON parent.name = child.parent 
			JOIN
				`tabTarea` AS task 
				ON child.task = task.name 
		WHERE
			parent.name = %s
			""", (task), as_dict=True)

@frappe.whitelist()
def has_any_open(task):
	if not frappe.get_value("Tarea", task, "dependant"):
		return frappe._dict({ "has_any_open": 0 })

	for task in get_task_status_list(task):
		if not task.status == "Closed":
			return frappe._dict({ "has_any_open": 1 })
	else:
		return frappe._dict({ "has_any_open": 0 })
