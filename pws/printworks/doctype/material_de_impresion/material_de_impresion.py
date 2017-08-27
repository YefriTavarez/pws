# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import pws.api

class MaterialdeImpresion(Document):
	def autoname(self):
		self.name = get_new_name(self)

def get_new_name(material_doc):
	name_sanitized = pws.api.s_sanitize(material_doc.get("nombre"))
	
	new_name = "{0}".format(name_sanitized)

	if material_doc.get("calibre"):
		new_name = "{0} {1}".format(new_name, material_doc.get("calibre"))

	if material_doc.get("cara"):
		new_name = "{0} {1}c".format(new_name, material_doc.get("caras"))

	# return as title ex. the egg pla
	return new_name.title()

@frappe.whitelist()
def rename_doc(frm_doc):
	doc = frappe.json.loads(frm_doc)

	if not doc.get("name") == get_new_name(doc):
		return frappe.rename_doc("Material de Impresion", 
			doc.get("name"), get_new_name(doc), force=True)
