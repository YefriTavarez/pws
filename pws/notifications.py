import frappe

def get_notification_config():
	return {
		"for_doctype": {
			"Tarea": {"status": ["!=", "Closed"], "user": frappe.session.user},
		},
		"for_other": {
			# todo
		}
	}
