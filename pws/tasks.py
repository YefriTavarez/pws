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

	project_list = frappe.get_list("Proyecto", {
		"status": "Open",
		"creation": [">=", str(a_month_ago)]
	}, ["name"])

	for project in project_list:
		prev_task = frappe._dict({})
		project_doc = frappe.get_doc("Proyecto", project.name)

		task_list = [ t for t in project_doc.tasks if not t.status == 'Closed' and not status == 'Cancelled']

		for task in task_list:
			doc = frappe.get_doc("Tarea", task.task_id)
			
			if task.dependant:
				if not prev_task.get("close_date"): break

				opts = frappe._dict({
					"as_datetime": True,
					"date": prev_task.get("close_date"),
					task.time_unit: task.max_time
				})

				exp_end_date = add_to_date(**opts)

				if not str(exp_end_date) == str(doc.exp_end_date):
					if prev_task.get("close_date") > doc.exp_start_date:
						doc.exp_start_date = prev_task.get("close_date")
						doc.exp_end_date = exp_end_date
						doc.db_update()

						task.start_date = prev_task.get("close_date")
						task.end_date = exp_end_date
						task.db_update()

			elif doc.exp_end_date < frappe.utils.now_datetime():
				doc.status = "Overdue"
				doc.db_update()

				task.status = "Overdue"
				task.db_update()
				
			prev_task = task
			

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
