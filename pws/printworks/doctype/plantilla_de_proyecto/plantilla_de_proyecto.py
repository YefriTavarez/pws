# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.model.mapper import get_mapped_doc as map_doc

class PlantilladeProyecto(Document):
	def create_project(self):
		new_project = frappe.new_doc("Proyecto")

		doclist = map_doc(self.doctype, self.name, {
		    "Plantilla de Proyecto": {
		        "doctype": "Proyecto",
		        "field_map": {
		            # nothing
		        }
		    }
		}, new_project)

		# new_project.save()
		
		return doclist
