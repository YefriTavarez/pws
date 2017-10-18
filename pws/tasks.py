# -*- coding: utf-8 -*-

import frappe
from frappe.utils import now_datetime, flt

def all():
	update_task_start_times()

def hourly():
	set_as_completed_projects()

def daily():
	close_projects()

def weekly():
	pass

def monthly():
	pass

def update_task_start_times():
	from pws.api import add_to_date

	a_month_ago = add_to_date(now_datetime(), months=-1)

	no_closed_task_list = frappe.get_list("Tarea", {
		"status": ["!=", "Closed"],
		"creation": [">=", str(a_month_ago)] # to speed up this process
	}, ["name"], order_by="project")

	for cur_dict in no_closed_task_list:
		task = frappe.get_doc("Tarea", cur_dict.name)
		
		if flt(task.dependant):
			opts = frappe._dict({
				"as_datetime": True,
				"date": get_latest_close_date(task),
				task.time_unit: task.max_time
			})

			exp_end_date = add_to_date(**opts)

			# check if it is not updated yet
			if not exp_end_date == task.exp_end_date:
				if not task.exp_end_date or task.exp_end_date < now_datetime():
					task.exp_start_date = get_latest_close_date(task)
					task.exp_end_date = exp_end_date
					task.db_update()
				
			elif not is_there_any_pending_task(task) and task.exp_end_date < now_datetime():
				task.status = "Overdue"
				task.db_update()

		elif task.exp_end_date < frappe.utils.now_datetime():
			task.status = "Overdue"
			task.db_update()

def close_projects():
	from pws.api import add_to_date

	a_month_ago = add_to_date(now_datetime(), months=-1)

	project_list = frappe.get_list("Proyecto", {
		"status": "Open",
		"creation": ["<=", str(a_month_ago)]
	})

	for project in project_list:
		doc = frappe.get_doc("Proyecto", project.name)

		doc.status = "Cancelled"

		doc.add_comment("Edit", "Proyecto cerrado por el Administrador de Proyectos")
		doc.db_update()

def get_latest_close_date(task):
	return frappe.db.sql("""SELECT
		MAX(tarea_dependiente.close_date) 
	FROM
		`tabTarea Dependiente de` AS dependiente 
		JOIN
			tabTarea AS current 
			ON current.name = dependiente.parent 
		JOIN
			tabTarea AS tarea_dependiente 
			ON dependiente.task = tarea_dependiente.name 
	WHERE
		current.name = %s""", (task.name))[0][0]

def is_there_any_pending_task(task):
	is_there_one = False

	for dependee in task.depends_on:
		task_status = frappe.get_value("Tarea", dependee.get("task"), "status")
		
		if not task_status == "Closed":
			return True

	return is_there_one

def set_as_completed_projects():
	project_list = frappe.get_list("Proyecto", {
		"status": "Open"
	})

	for current in project_list:
		project = frappe.get_doc("Proyecto", current.name)

		project.onload()

		if not [task for task in project.tasks if not task.status == 'Closed']:
			project.set('status', 'Completed')
		else:
			project.set('status', 'Open')

		project.db_update()

