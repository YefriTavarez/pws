import frappe

def get_notification_config():
	return {
		"for_doctype": {
			"Tarea": "pws.notifications.get_things_to_do",
			"Opportunity": {"docstatus": [">=", "2"]},
			"Customer": {"docstatus": [">=", "2"]},
			"Quotation": {"docstatus": ["=", "0"]},
			"Sales Order": {"docstatus": ["=", "0"]},
			"Sales Invoice": {"docstatus": ["=", "0"]},
			"Delivery Note": {"docstatus": ["=", "0"]},
			"Purchase Order": {"docstatus": ["=", "0"]},
			"Purchase Invoice": {"docstatus": ["=", "0"]},
			"Purchase Receipt": {"docstatus": ["=", "0"]},
			"Solicitud de Diligencia": "pws.notifications.get_solicitudes_de_diligencias",
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

def get_solicitudes_de_diligencias():
	if frappe.has_permission("Solicitud de Diligencia", "submit", user=frappe.session.user):
		return frappe.get_value("Solicitud de Diligencia", {
			"status": ["=", "PENDIENTE"]
		}, ["count(name)"])

	return 0.000
