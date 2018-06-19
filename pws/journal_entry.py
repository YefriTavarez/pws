import frappe

def on_submit(doc, event):
	if frappe.db.exists("Solicitud de Pago", doc.solicitud_de_pago):
		sol = frappe.get_doc("Solicitud de Pago", doc.solicitud_de_pago)
		sol.outstanding_amount = 0.000

		sol.db_update()
		frappe.db.commit()

def on_cancel(doc, event):
	if frappe.db.exists("Solicitud de Pago", doc.solicitud_de_pago):
		sol = frappe.get_doc("Solicitud de Pago", doc.solicitud_de_pago)
		sol.outstanding_amount = sol.approved_amount

		sol.db_update()
		frappe.db.commit()
		