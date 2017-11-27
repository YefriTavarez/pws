import frappe

def get_task_list(boot_info):
	boot_info.task_list = frappe.get_all("Tarea", filters={
		# empty filters
	}, fields=["distinct subject"], order_by="idx", as_list=True)