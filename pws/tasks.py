# -*- coding: utf-8 -*-

import frappe
from frappe.utils import now_datetime

def all():
	update_task_start_times()

def hourly():
	pass

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
		
		if task.dependant:
			opts = frappe._dict({
				"as_datetime": True,
				"date": get_latest_close_date(task),
				task.time_unit: task.max_time
			})

			exp_end_date = add_to_date(**opts)

			# check if it is not updated yet
			if not exp_end_date == task.exp_end_date:
				if not task.exp_start_date or task.exp_start_date > now_datetime():
					task.exp_start_date = get_latest_close_date(task)
					task.exp_end_date = exp_end_date
					task.db_update()
				
			if not is_there_any_pending_task(task):
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
	latest_close_date = None

	for dependee in task.depends_on:
		task_closed_date = frappe.get_value("Tarea", dependee.get("task"), "close_date")

		if not latest_close_date or latest_close_date < task_closed_date:
			latest_close_date = task_closed_date

	return latest_close_date

def is_there_any_pending_task(task):
	is_there_one = False

	for dependee in task.depends_on:
		task_status = frappe.get_value("Tarea", dependee.get("task"), "status")
		is_there_one = not task_status == "Closed"

	return is_there_one

