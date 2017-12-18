import frappe

def get_task_list(boot_info):
	boot_info.task_list = frappe.get_all("Tarea", filters={
		# empty filters
	}, fields=["distinct subject"], order_by="idx", as_list=True)

def add_user_info(boot_info):
	user_department	= frappe.get_value("Employee", {
		"user_id": frappe.session.user
	}, "department")
	
	user_department and boot_info.user.update({
		"department": user_department
	})