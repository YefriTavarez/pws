# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import pws.api

from frappe.model.document import Document

_item_group = frappe.db.get_single_value("Configuracion General", "item_group")

class PerfiladordeProductos(Document):
	def validate(self):
		self.create_item_group_if_not_exists()

	def before_rename(self, doctype, old_name, new_name):
		self.old_item_name = "{0}".format(self.name)

		self.db_update()

	def after_rename(self, doctype, old_name, new_name):
		frappe.rename_doc("Item Group", self.old_item_name,
			"{0}".format(self.name))

		self.item_group = "{0}".format(self.name)

		self.db_update()

	def create_item_group_if_not_exists(self):
		doc = frappe.new_doc("Item Group")

		item_group = frappe.get_value("Item Group", {
			"item_group_name": self.name
		}, ["name"])

		if item_group:
			doc = frappe.get_doc("Item Group", item_group)

		doc.update({
			"parent_item_group" : _item_group,
			"item_group_name" : self.name,
			"route": self.get_route(),
			"is_group": False
		})

		doc.save()

		# # update this object too
		# self.item_group = doc.item_group_name
		# self.parent_item_group = doc.parent_item_group

	def get_route(self):
		parent_route = ''

		parent_route = frappe.get_value("Item Group", 
			_item_group, "route")

		item_group_route = pws.api.s_strip("{0}".format(self.name))

		return "{0}/{1}".format(parent_route, item_group_route.lower())

	def on_trash(self):
		frappe.delete_doc_if_exists("Item Group", self.name, force=True)
