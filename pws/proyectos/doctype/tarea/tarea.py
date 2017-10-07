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

				status = frappe.get_value("Task", dependee.task, "status")

				if not status == "Closed" and not status == "Cancelled":
					frappe.throw(message)

		# proyecto.add_comment("Edit", "{} cerro la tarea {} a las {}".format(frappe.session.user, "01", frappe.utils.now_datetime()), frappe.session.user, "Tarea", "TAREA-001")

