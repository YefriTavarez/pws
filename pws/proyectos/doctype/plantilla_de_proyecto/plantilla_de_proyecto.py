# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.model.mapper import get_mapped_doc as map_doc

class PlantilladeProyecto(Document):
	def validate(self):
		self.create_project_type_if_not_exists()

	def create_project(self):
		return map_doc(self.doctype, self.name, {
			self.doctype: {
				"doctype": "Proyecto",
				"field_map": {
					"template_name": "project_name"
				}
			},
			"Tarea de Plantilla": {
				"doctype": "Tarea de Proyecto",
				"field_map": {
					# to do
				}
			}
		}, frappe.new_doc("Proyecto"))

	def create_project_type_if_not_exists(self):
		doc = frappe.new_doc("Tipo de Proyecto")

		project_type = frappe.get_value("Tipo de Proyecto", {
			"project_type": self.name
		}, ["name"])

		if project_type:
			doc = frappe.get_doc("Tipo de Proyecto", project_type)

		doc.update({
			"project_type" : self.name,
		})

		doc.save()

		# update this object too
		self.project_type = doc.project_type

	def on_trash(self):
		try:
			frappe.delete_doc("Tipo de Proyecto", self.project_type)
		except:
			pass # just ignore it as there is at least one project using it
