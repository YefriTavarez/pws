# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe, json

from pws.api import s_sanitize, gut
from frappe.model.document import Document
from frappe.utils.file_manager import save_file

from frappe.model.mapper import get_mapped_doc as map_doc
from frappe.model.naming import make_autoname as autoname

class Proyecto(Document):
	def __setup__(self):
		pass
		# self.make_difference()

	def autoname(self):

		name_sanitized = s_sanitize(self.project_type)

		first_two = gut(name_sanitized, size=3)

		naming_serie = "{0}-.#####".format(*first_two)

		self.name = autoname(naming_serie)
	
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
					"template_name": "project_name"
				}
			},
			"Tarea de Plantilla": {
				"doctype": "Tarea de Proyecto",
				"field_map": {
					# to do
				}
			}
		}, self)

	def sync_tasks(self):
		task_names = []

		for task in self.tasks:
			doc = sync_task(task, self.name)

			task.task_id = doc.name
			task_names.append(task.task_id)

			task.db_update()

		# delete
		for task in frappe.get_all("Tarea", ["name"], {"proyecto": self.name, "name": ("not in", task_names)}):
			frappe.delete_doc("Tarea", task.name)

	# def make_difference(self):
	# 	task_names = []

	# 	for task in frappe.get_all("Tarea", ["name"], { "proyecto": self.name }):
	# 		task_names.append(task.name)

	# 	for task in self.get_project_tasks():
	# 		if not task.task_id in task_names:
	# 			frappe.delete_doc("Tarea de Proyecto", task.name)

	# 	frappe.db.commit() 

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
		"task_weight": task.task_weight,
		"user": task.user
	})

	doc.save(ignore_permissions=True)

	return doc
