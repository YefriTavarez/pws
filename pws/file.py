import frappe

def after_insert(doc, event):
	if doc.attached_to_doctype == "Proyecto":
		doc.content_hash = None
		doc.db_update()
	else: pass