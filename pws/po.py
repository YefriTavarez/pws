import frappe

from frappe.utils import flt, cint, cstr
from frappe.utils import add_to_date, now_datetime

def on_submit(doc, event):
	if event == "on_submit":
		doc.validado_por = " ".join(frappe.get_value("User", 
			frappe.session.user, ["first_name", "last_name"]))

		doc.db_update()
		frappe.db.commit()

@frappe.whitelist()
def make_payment_request(doctype, docname):
	doc = frappe.get_doc(doctype, docname)

	payment_request = frappe.new_doc("Solicitud de Pago")

	description = """Pago de compra de Materiales / Servicios a proveedores
		\nOrden de Compra No. {docname}""".format(docname=docname)

	payment_request.update({
		u'approved_amount': doc.grand_total,
		u'currency': doc.currency,
		u'motivation': description,
		u'party_type': "Supplier",
		u'party': doc.supplier,
		u'requested_amount': doc.grand_total,
		u'required_before': add_to_date(now_datetime(), hours=1),
		u'transaction_type': doc.doctype,
		u'transaction_name': doc.name,
 	})

	return payment_request
