# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import pws.api
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

	def on_update(self):
		from pws.api import s_strip

		material_list = frappe.get_list("Material de Impresion Items", {
			"parent": self.name,
			"parenttype": "Dimension",
			"parentfield": "materials",
		}, ["materials", "parent"])
	
		for material in material_list:
			material_doc = frappe.get_doc("Material de Impresion", material.materials)
			item_code = "{0}{1}".format(material.materials, s_strip(self.name))

			item_doc = frappe.new_doc("Item")
			item_group = pws.api.get_materials_item_group()

			if frappe.get_value("Item", item_code):
				item_doc = frappe.get_doc("Item", item_code)

			item_doc.update({
				"item_code": item_code,
				"item_name": material_doc.full_name,
				"item_group": item_group,
				"is_sales_item": 0,
				"is_purchase_item": 1,
				"description": "{0} en {1}".format(material_doc.full_name, self.name)
			})

			item_doc.save()
				
		frappe.db.commit()

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

	def on_trash(self):
		material_list = frappe.get_list("Material de Impresion Items", {
			"parent": self.name,
			"parenttype": "Dimension",
			"parentfield": "materials",
		}, ["materials", "parent"])
	
		for material in material_list:
			item_name = "{materials}, {parent}".format(**material)

			frappe.delete_doc_if_exists("Item", item_name)
