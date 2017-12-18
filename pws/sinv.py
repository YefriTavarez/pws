import frappe

from frappe.utils import cint

def sinv_autoname(doc, event):
	from frappe.model.naming import make_autoname
	doc.name = make_autoname("FACT-.#####")

	if doc.is_return:
		doc.return_against_ncf = doc.ncf

	if not doc.ncf or cint(doc.is_return):
		doc.ncf = make_autoname(doc.naming_series)