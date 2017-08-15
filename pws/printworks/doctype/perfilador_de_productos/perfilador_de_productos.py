# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

_item_group = frappe.db.get_single_value("Stock Settings", "item_group")

class PerfiladordeProductos(Document):
	def validate(self):
		item_group = frappe.get_value("Item Group", {
			"item_group_name": "- {0}".format(self.name)
		})

		if not item_group:
			self.create_item_group()

	def before_rename(self, doctype, old_name, new_name):
		self.old_item_name = self.name
		self.item_group = "- {0}".format(self.name)

		self.db_update()

	def after_rename(self, doctype, old_name, new_name):
		frappe.rename_doc("Item Group", "- {0}".format(self.old_item_name), 
			"- {0}".format(self.name))

		self.db_update()

	def create_item_group(self):
		item_group = frappe.new_doc("Item Group")

		item_group.parent_item_group = _item_group
		item_group.item_group_name = "- {0}".format(self.name)

		item_group.insert()

		# update this object too
		self.item_group = item_group.item_group_name
		self.parent_item_group = item_group.parent_item_group

	def on_trash(self):
		frappe.delete_doc("Item Group", self.item_group, force=True)
