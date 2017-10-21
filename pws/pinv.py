import frappe


def validate(doc, event):
	for item in doc.items:
		item.amount = flt(item.amount, 2)
