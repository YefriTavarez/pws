# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MaterialdeImpresion(Document):
	def autoname(self):
		self.name = get_new_name(self)

def get_new_name(material_doc):
	name = "{0}".format(material_doc.get("nombre").replace(" ", "-"))

	if material_doc.get("calibre"):
		name = "{0}-{1}".format(name, material_doc.get("calibre"))

	if material_doc.get("cara"):
		name = "{0}-{1}c".format(name, material_doc.get("caras"))

	return name.upper()

@frappe.whitelist()
def rename_doc(frm_doc):
	doc = frappe.json.loads(frm_doc)

	if not doc.get("name") == get_new_name(doc):
		return frappe.rename_doc("Material de Impresion", 
			doc.get("name"), get_new_name(doc), force=True)
