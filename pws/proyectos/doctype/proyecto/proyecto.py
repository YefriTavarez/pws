# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe, json

from pws.api import s_sanitize, gut
from frappe.model.document import Document
from frappe.utils.file_manager import save_file

from frappe.desk.form.assign_to import add as assign_to
from frappe.model.mapper import get_mapped_doc as map_doc
from frappe.model.naming import make_autoname as autoname

class Proyecto(Document):
	def onload(self):
		for task in self.tasks:
			doc = frappe.get_doc("Tarea", task.task_id)

			task.update({
				"title": doc.subject,
				"status": doc.status,
				"start_date": doc.exp_start_date,
				"end_date": doc.exp_end_date,
				"description": doc.description,
				"user": doc.user,
				"task_id": doc.name,
				"dependant": doc.dependant,
				"close_date": doc.close_date,
			})

	def autoname(self):
		name_sanitized = s_sanitize(self.project_type)

		first_two = gut(name_sanitized, size=3)

		naming_serie = "{0}-.#####".format(*first_two)

		self.name = autoname(naming_serie)

	def after_insert(self):
		assign_to({
			"doctype": self.doctype,
			"name": self.name,
			"assign_to": self.project_manager,
			"description": "El proyecto {0} ({1}) ha sido encargado a usted"
				.format(self.name, self.project_name)
			})
	
	def on_update(self):
		self.sync_tasks()

		pending_task = False

		for task in self.tasks:
			if not task.status == "Closed":
				pending_task = True

		if not pending_task:
			self.status = "Completed"

		self.db_update()

	def validate(self):
		dirty_name = self.collect_names()

		name_sanitized = s_sanitize(dirty_name)

		self.title = name_sanitized.title()

		closed_tasks = len([task for task in self.tasks if task.status == "Closed"])
		not_closed_tasks = len([task for task in self.tasks if task.status != "Cancelled" and task.status != "Closed"])

		self.percent_complete = closed_tasks / (not_closed_tasks or 1.000) * 100.000

	def collect_names(self):
		fields = ["project_type", "customer", "item_name", 
			"project_name", "production_qty"]

		return "{0}: {1} {2} ({3}) Cant. {4}".format(*[
			self.get(field) for field in fields])

	def create_project(self):
		self.set("tasks", [])
		
		return map_doc("Plantilla de Proyecto", self.plantilla_de_proyecto, {
			"Plantilla de Proyecto": {
				"doctype": "Proyecto",
				"field_map": {
					# to do
				}
			},
			"Tarea de Plantilla": {
				"doctype": "Tarea de Proyecto",
				"field_map": {
					# to do
				}
			}
		}, self)

		self.set("project_name", [])

	def sync_tasks(self):
		task_names = []

		for task in self.tasks:
			doc = sync_task(task, self.name)

			task.task_id = doc.name
			task_names.append(task.task_id)

			task.db_update()

		for task in self.tasks:
			doc = frappe.get_doc("Tarea", task.task_id)
			if doc.dependant:

				doc.set("depends_on", [])
				
				for title in (task.depends_on or "").split(", "):
					if not title: break
					
					d = frappe.get_doc("Tarea", {
						"subject": title,
						"proyecto": self.name
					})

					doc.append("depends_on", {
						"task": d.name,
						"subject": d.subject,
						"project": d.project
					})
				doc.save()


		# delete
		for task in frappe.get_all("Tarea", ["name"], {"proyecto": self.name, "name": ("not in", task_names)}):
			frappe.delete_doc("Tarea", task.name)

	def get_project_tasks(self):
		return frappe.get_all("Tarea de Proyecto", { 
			"parent": self.name 
		}, ["task_id", "name"])


	def on_trash(self):
		tasks = frappe.get_all("Tarea", {
			"proyecto": self.name 
		}, ["name"])

		for task in tasks:
			frappe.delete_doc("Tarea", task.name, force=True)

@frappe.whitelist()
def attach_file(doctype, docname, filedata):
	if not filedata: return

	fd_json = json.loads(filedata)
	fd_list = list(fd_json["files_data"])

	for fd in fd_list:
		file_list = frappe.get_list("File", { "file_name": ["like", "{}%".format(fd["filename"])]})

		if file_list:
			fd["filename"] = fd["filename"].replace(".pdf", "-{}.pdf".format(len(file_list) +1))

		filedoc = save_file(fd["filename"], fd["dataurl"], 
			doctype, docname, decode=True, is_private=True)

def sync_task(task, project_name):
	doc = frappe.new_doc("Tarea")
	
	if frappe.get_value("Tarea", task.task_id):
		doc = frappe.get_doc("Tarea", task.task_id)

	doc.update({
		"proyecto": project_name,
		"subject": task.title,
		"status": task.status,
		"exp_start_date": task.start_date,
		"exp_end_date": task.end_date,
		"description": task.description,
		"user": task.user,
		"dependant": task.dependant
	})

	doc.save(ignore_permissions=True)

	return doc