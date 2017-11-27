# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.contacts.doctype.address.address import address_query
from frappe.contacts.doctype.address.address import get_address_display
from frappe.contacts.doctype.address.address import get_default_address

class SolicituddeDiligencia(Document):
	def after_insert(self):
		self.user = self.owner
		self.db_update()

	def validate(self):
		if self.is_new() and not self.status == "PENDIENTE":
			frappe.throw("Debe guardar primero antes de aprobar o denegar.")
		
		if self.is_new():
			return 0
			
		if not frappe.has_permission(self.doctype, "submit", user=frappe.session.user)\
			and not self.status == "PENDIENTE":
			frappe.throw("No tiene permitido aprobar ni denegar esta Solicitud de Diligencia.")

		if self.status == "DENEGADO" and not self.notes:
			frappe.throw("Justifique en las notas porque se denego la solicitud.")

		if not self.status == "PENDIENTE" and frappe.has_permission(self.doctype, "submit", user=frappe.session.user):
			self.docstatus = 1
			self.set_docstatus()
			self.db_update()

	def submit(self):
		if self.status == "PENDIENTE":
			frappe.throw("Debe aprobar o denegar esta Solicitud de Diligencia antes de validarla.")

		if self.status == "DENEGADO" and not self.notes:
			frappe.throw("Justifique en las notas porque se denego la solicitud.")

	def update_address(self):
		# exit if one of the two fields are not present
		if not self.party_type or not self.party: return

		self.party_address = get_default_address(self.party_type, self.party)

		if self.party_address:
			self.display_address = get_address_display(self.party_address)
		else:
			self.display_address = None