# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Dimension(Document):
	def autoname(self):
		new_name = "{width} {uom} x {height} {uom}".format(
			** self.as_dict())

		self.name = new_name

	def validate(self):
		self.area = self.width * self.height
