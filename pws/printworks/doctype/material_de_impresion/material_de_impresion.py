# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MaterialdeImpresion(Document):
	def autoname(self):
		name = "{0}".format(self.nombre.replace(" ", "-"))

		if self.calibre:
			name = "{0}-{1}".format(name, self.calibre)

		if self.cara:
			name = "{0}-{1}c".format(name, self.caras)

		self.name = name.upper()
