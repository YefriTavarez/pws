import frappe

from frappe.utils import cint

def autoname(doc, event):
	doc.employee_number = next_employee_number()
	doc.name = "{0}".format(doc.employee_number)

def next_employee_number():
	return cint(top_employee_number()) + 1

def top_employee_number():
	return frappe.db.sql("select max(employee_number) from tabEmployee")[0][0]