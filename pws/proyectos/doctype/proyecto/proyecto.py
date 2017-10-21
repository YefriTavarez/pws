# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe, json

from frappe.utils import flt
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

		self.update_percent_complete()
		self.update_costs()

	def autoname(self):
		# name_sanitized = s_sanitize(self.project_type)

		# first_two = gut(name_sanitized, size=3)

		naming_serie = "PROY-.#####"

		self.name = autoname(naming_serie)
	
	def after_insert(self):
		self.sync_tasks()

		pending_task = False

		for task in self.tasks:
			if not task.status == "Closed":
				pending_task = True

		if not pending_task:
			self.status = "Completed"

		self.db_update()

	def validate(self):
		name_sanitized = self.collect_names()

		self.title = name_sanitized

	def update_percent_complete(self):

		closed_tasks = len([task for task in self.tasks if task.status == "Closed"])
		not_closed_tasks = len([task for task in self.tasks if task.status != "Cancelled"])

		self.percent_complete = flt(closed_tasks) / (not_closed_tasks or 1.000) * 100.000

	def collect_names(self):
		self.item_name = frappe.get_value("Item", self.item, "item_name")		
		if "," in self.item_name:
			arr = self.item_name.split(',', 1)
			
			self.item_name = "{0} ({1}), {2}".format(arr[0], self.project_name, arr[1])
		else:
			self.item_name = "{0} ({1})".format(self.item_name, self.project_name)

		fields = ["project_type", "customer", "item_name", 
			"production_qty"]

		return "{0}: {1} - {2}, Cant. {3}".format(*[
			s_sanitize(self.get(field), upper=False) for field in fields])

	def update_costs(self):
		self.total_purchase_cost = frappe.db.sql("""SELECT 
				SUM(child.amount)
			FROM `tabPurchase Invoice Item` as child 
			JOIN `tabPurchase Invoice` as parent
			ON parent.name = child.parent
			WHERE parent.docstatus = 1
			AND child.proyecto = %s
		""", (self.name))[0][0]

		self.total_purchase_order_cost = frappe.db.sql("""SELECT
				SUM(child.amount) 
			FROM
				`tabPurchase Order Item` AS child 
				JOIN
					`tabPurchase Order` AS parent 
					ON child.parent = parent.name 
			WHERE
				parent.docstatus = 1 
				AND child.proyecto = %s """, (self.name))[0][0]

		self.total_sales_cost = frappe.db.sql("""SELECT
				SUM(child.amount) 
			FROM
				`tabSales Order Item` AS child 
				JOIN
					`tabSales Order` AS parent 
					ON child.parent = parent.name 
			WHERE
				parent.docstatus = 1 
				AND child.proyecto = %s""", (self.name))[0][0]

		# self.total_sales_invoice_cost = frappe.db.sql("""SELECT
		# 		SUM(total) 
		# 	FROM
		# 		`tabSales Invoice` 
		# 	WHERE
		# 		docstatus = 1 
		# 		AND proyecto = %s""", (self.name))[0][0]

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
			doc.project_name = self.title

			task.task_id = doc.name
			task_names.append(task.task_id)

			doc.db_update()
			task.db_update()

		for task in self.tasks:
			doc = frappe.get_doc("Tarea", task.task_id)
			if doc.dependant:

				doc.set("depends_on", [])
				
				for title in (task.depends_on or "").split(", "):
					if not title: break
					
					d = frappe.get_doc("Tarea", {
						"subject": title,
						"project": self.name
					})

					doc.append("depends_on", {
						"task": d.name,
						"subject": d.subject,
						"project": d.project
					})

				doc.save()

		# # delete
		# for task in frappe.get_all("Tarea", ["name"], {"project": self.name, "name": ("not in", task_names)}):
		# 	frappe.delete_doc("Tarea", task.name)

	def get_project_tasks(self):
		return frappe.get_all("Tarea de Proyecto", { 
			"parent": self.name 
		}, ["task_id", "name"])


	def on_trash(self):
		tasks = frappe.get_all("Tarea", {
			"project": self.name 
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
		"project": project_name,
		"subject": task.title,
		"status": task.status,
		"exp_start_date": task.start_date,
		"exp_end_date": task.end_date,
		"description": task.description,
		"user": task.user,
		"dependant": task.dependant,
		"owner": task.user,
		"time_unit": task.time_unit,
		"max_time": task.max_time
	})

	doc.save(ignore_permissions=True)

	return doc