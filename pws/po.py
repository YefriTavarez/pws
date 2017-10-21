import frappe

def on_submit(doc, event):
	if event == "on_submit":
		doc.validado_por = " ".join(frappe.get_value("User", 
			frappe.session.user, ["first_name", "last_name"]))

		doc.db_update()
		frappe.db.commit()
