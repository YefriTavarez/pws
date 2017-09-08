# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.utils import flt
import pws.api

class MaterialdeImpresion(Document):
	def autoname(self):
		self.name = self.make_new_name()

	def validate(self):
		full_name = "{}".format(
			self.nombre)

		if flt(self.calibre):
			full_name = "{} {}".format(full_name, self.calibre)

		if flt(self.caras):
			full_name = "{} {}C".format(full_name, self.caras)

		self.full_name = full_name.title()

	def on_update(self):
		from  pws.api import s_strip

		dimension_list = frappe.get_list("Material de Impresion Items", {
			"materials": self.name,
			"parenttype": "Dimension",
			"parentfield": "materials",
		}, ["parent"])
	
		for dimension in dimension_list:
			item_code = "{0}{1}".format(self.name, s_strip(dimension.parent))

			item_doc = frappe.new_doc("Item")
			item_group = pws.api.get_materials_item_group()

			if frappe.get_value("Item", item_code):
				item_doc = frappe.get_doc("Item", item_code)

			item_doc.update({
				"item_code": item_code,
				"item_name": self.full_name,
				"item_group": item_group,
				"is_sales_item": 0,
				"is_purchase_item": 1,
				"description": "{0} en {1}".format(self.full_name, dimension.parent)
			})

			item_doc.save()
				
		frappe.db.commit()


	def make_new_name(self):
		return get_new_name(self)

def get_new_name(material_doc):
	name_sanitized = pws.api.s_sanitize(material_doc.get("nombre"))
	gutted = pws.api.gut(name_sanitized)
	
	new_name = "{0}".format("".join(gutted))

	if material_doc.get("calibre"):
		new_name = "{0}{1}".format(new_name, material_doc.get("calibre"))

	if material_doc.get("cara"):
		new_name = "{0}{1}c".format(new_name, material_doc.get("caras"))

	return new_name.upper()

@frappe.whitelist()
def rename_doc(frm_doc):
	doc = frappe.json.loads(frm_doc)

	if not doc.get("name") == get_new_name(doc):
		return frappe.rename_doc("Material de Impresion", 
			doc.get("name"), get_new_name(doc), force=True)
