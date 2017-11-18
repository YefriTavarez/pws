import frappe

def validate(doc, event):
	if not doc.tax_id:
		doc.tax_id = frappe.get_value("Customer", doc.customer, "tax_id")