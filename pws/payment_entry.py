import frappe

def on_submit(doc, event):
	if not doc.payment_request: return

	sol = frappe.get_doc("Solicitud de Pago", doc.payment_request)
	sol.outstanding_amount = 0

	sol.reference_name = doc.reference_no
	sol.reference_date = doc.reference_date

	sol.db_update()
	frappe.db.commit()


def on_cancel(doc, event):
	if not doc.payment_request: return
	
	sol = frappe.get_doc("Solicitud de Pago", doc.payment_request)
	sol.outstanding_amount = sol.approved_amount

	sol.reference_name = ""
	sol.reference_date = ""
	
	sol.db_update()
	frappe.db.commit()
	