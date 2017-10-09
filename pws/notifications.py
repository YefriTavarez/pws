import frappe

def get_notification_config():
	return {
		"for_doctype": {
			"Tarea": "pws.notifications.get_things_to_do",
		},
		"for_other": {
			# todo
		}
	}

def get_things_to_do():
	return frappe.db.sql("""SELECT COUNT(*)
		FROM `tabTarea`
		WHERE user = '%(user)s'
			AND status <> 'Closed' """ % { "user": frappe.session.user },
	as_list=True)[0][0]
