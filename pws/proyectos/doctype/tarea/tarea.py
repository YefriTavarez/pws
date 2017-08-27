# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.desk.form.assign_to import add as assign

class Tarea(Document):
	def after_insert(self):
		self.user and self.assign_to()

	def assign_to(self):
		assign({
			"assign_to": self.user,
			"doctype": self.doctype,
			"name": self.name,
			"description": self.subject
		})
