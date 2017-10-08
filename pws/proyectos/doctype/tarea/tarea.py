# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document

from frappe.desk.form.assign_to import add as assign

message = "¡Estado de la Tarea no se puede cambiar mientras hayan tareas incompletas!"

class Tarea(Document):
	# def after_insert(self):
	# 	self.user and self.assign_to()

	def assign_to(self):
		assign({
			"assign_to": self.user,
			"doctype": self.doctype,
			"name": self.name,
			"description": self.subject
		})

	def validate(self):
		if self.dependant and not self.status == "Open": 
			for dependee in self.depends_on:

				status = frappe.get_value("Tarea", dependee.task, "status")

				if not status == "Closed" and not status == "Cancelled":
					frappe.throw(message)

		if self.get("was_closed"):
			self.after_validate()

	def after_validate(self):
		project = frappe.get_doc("Proyecto", self.project)

		task_number = frappe.get_value("Tarea de Proyecto", {
			"parent": project.name,
			"task_id": self.name
		}, ["idx"])

		msg = u"Cerró la tarea {0} a las {1}".format(task_number, 
			frappe.utils.now_datetime())

		project.add_comment("Edit", msg, frappe.session.user, self.doctype, self.name)

		project.db_update()

