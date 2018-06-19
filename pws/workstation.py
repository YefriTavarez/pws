import frappe

def autoname(doc, event):
	if not doc.workstation_code:
		frappe.throw("Falta el codigo")

	doc.name = doc.workstation_code
