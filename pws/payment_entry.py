import frappe

def on_submit(doc, event):
	if doc.payment_request:

		sol = frappe.get_doc("Solicitud de Pago", doc.payment_request)
		sol.outstanding_amount = 0

		sol.reference_name = doc.reference_no
		sol.reference_date = doc.reference_date

		sol.db_update()
		frappe.db.commit()

	if len(doc.solicitudes_de_pago):
		for row in doc.solicitudes_de_pago:
			sol = frappe.get_doc("Solicitud de Pago", row.payment_request)
			sol.outstanding_amount = 0

			sol.reference_name = doc.reference_no
			sol.reference_date = doc.reference_date

			sol.db_update()
			frappe.db.commit()

def on_cancel(doc, event):
	if doc.payment_request:	
		sol = frappe.get_doc("Solicitud de Pago", doc.payment_request)
		sol.outstanding_amount = sol.approved_amount

		sol.reference_name = ""
		sol.reference_date = ""
		
		sol.db_update()
		frappe.db.commit()

	if len(doc.solicitudes_de_pago):
		for row in doc.solicitudes_de_pago:
			sol = frappe.get_doc("Solicitud de Pago", row.payment_request)
			sol.outstanding_amount = sol.approved_amount

			sol.reference_name = ""
			sol.reference_date = ""
			
			sol.db_update()
			frappe.db.commit()
	
		