# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import pws.utils

from frappe.model.document import Document

class Dimension(Document):
	def autoname(self):
		new_name = self.make_new_name()

		self.name = new_name
		
	def validate(self):
		self.calculate_area()

		new_name = self.get_new_name()

		backward = self.get_backward_name()

		exists = frappe.get_value(self.doctype, new_name) or\
			frappe.get_value(self.doctype, backward)

		if exists and not new_name == self.name:
			frappe.throw("""Dimension <a href="{0}">{1}</a> ya existe"""
				.format(
					frappe.utils.get_url_to_form(self.doctype, new_name),
					new_name
				)
			)

	def calculate_area(self):
		self.area = self.width * self.height

	def make_new_name(self):

		backward = self.get_backward_name()

		if not backward == self.name and frappe.get_value(self.doctype, backward):
			frappe.throw("""Dimension <a href="{0}">{1}</a> ya existe"""
				.format(
					frappe.utils.get_url_to_form(self.doctype, backward),
					backward
				)
			)	

		return self.get_new_name()

	def get_new_name(self):
		return "{width} {uom} x {height} {uom}".format(
			** self.as_dict()
		)

	def get_backward_name(self):
		return "{height} {uom} x {width} {uom}".format(
			** self.as_dict()
		)
