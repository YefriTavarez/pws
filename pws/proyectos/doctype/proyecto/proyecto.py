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

		self.notify_project_manager()

	def validate(self):
		name_sanitized = self.collect_names()

		self.title = name_sanitized
		self.notify_project_manager_and_owner()

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
		self.get_total_purchase_invoice_cost()
		self.get_total_purchase_order_cost()
		self.get_total_sales_order_cost()
		self.get_total_sales_invoice_cost()

	def get_total_sales_invoice_cost(self):
		result = frappe.db.sql("""SELECT SUM(child.amount)
				FROM `tabProyecto` AS proyecto
			JOIN `tabSales Order` AS so
				ON proyecto.sales_order = so.name
			JOIN `tabSales Invoice Item` AS child
				ON child.sales_order = so.name
			WHERE proyecto = %(name)s
			AND child.docstatus = 1
			GROUP BY child.name""", self.as_dict(), as_list=True)

		if len(result):
			self.total_sales_invoice_cost = result[0][0]
		else:
			self.total_sales_invoice_cost = frappe.get_value("Sales Invoice Item", {
				"proyecto": self.name,
				"docstatus": 1
			}, ["SUM(amount)"])
			


	def get_total_sales_order_cost(self):
		self.total_sales_cost = frappe.get_value("Sales Order Item", {
			"proyecto": self.name,
			"docstatus": 1
		}, ["SUM(amount)"]) or\
		frappe.get_value("Sales Order", {
			"project": self.name,
			"docstatus": 1
		}, ["SUM(total)"]) or\
		frappe.get_value("Sales Order", {
			"name": self.sales_order,
			"docstatus": 1
		}, ["SUM(total)"])

	def get_total_purchase_invoice_cost(self):
		self.total_purchase_cost = frappe.get_value("Purchase Invoice Item", {
			"proyecto": self.name,
			"docstatus": 1
		}, ["SUM(amount)"])

	def get_total_purchase_order_cost(self):
		self.total_purchase_order_cost = frappe.get_value("Purchase Order Item", {
			"proyecto": self.name,
			"docstatus": 1
		}, ["SUM(amount)"])

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

	def notify_project_manager(self):
		from frappe import _
		__self__ = self.as_dict()
		__self__.owner_name = frappe.get_value("User", self.owner, "full_name")
		__self__.hostname = frappe.conf.get("hostname")

		opts = frappe._dict({
			"delayed": False,
			"recipients": [self.project_manager],
			"sender": frappe.get_value("Email Account", {"default_outgoing": "1"}, ["email_id"]),
			"reference_doctype": self.doctype,
			"reference_name": self.name,
			"subject": _("Nuevo Proyecto"),
			"message": _("""<i>%(owner_name)s</i> le ha asignado un nuevo Proyecto: <br>
				<a href="%(hostname)s/desk#Form/%(doctype)s/%(name)s">%(title)s</a>""" % __self__) 
		})

		frappe.sendmail(** opts)

	def notify_project_manager_and_owner(self):
		from frappe import _
		__self__ = self.as_dict()
		__self__.owner_name = frappe.get_value("User", self.modified_by, "full_name")
		__self__.hostname = frappe.conf.get("hostname")

		opts = frappe._dict({
			"delayed": False,
			"recipients": [self.project_manager],
			"sender": frappe.get_value("Email Account", {"default_outgoing": "1"}, ["email_id"]),
			"reference_doctype": self.doctype,
			"reference_name": self.name,
			"subject": _("Actualizacion de Proyecto"),
			"message": _("""<i>%(owner_name)s</i> ha modificado el Proyecto: <br>
				<a href="%(hostname)s/desk#Form/%(doctype)s/%(name)s">%(title)s</a>""" % __self__) 
		})

		frappe.sendmail(** opts)

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
		attach_type = frappe.get_value("Tipo de Adjunto", fd["attach_type"], 
			["allow_more_than_one", "max_attacthments"], as_dict=True)

		file_list = frappe.get_list("File", { "file_name": ["like", "{}%".format(fd["filename"].split(".pdf")[0])]})

		if file_list:
			if (not attach_type.allow_more_than_one and len(file_list))\
				or\
			(attach_type.allow_more_than_one and attach_type.max_attacthments 
				and flt(attach_type.max_attacthments) <= len(file_list)):
				frappe.throw("No puede agregar mas adjuntos de este tipo")

			fd["filename"] = fd["filename"].replace(".pdf", "-{}.pdf".format(len(file_list)))
			fd["filename"] = s_sanitize(fd["filename"], upper=False)
		
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