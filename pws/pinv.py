import frappe

from frappe.utils import flt

def validate(doc, event):
	for item in doc.items:
		item.amount = flt(item.amount, 2)
