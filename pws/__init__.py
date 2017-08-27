# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.0.1'

@frappe.whitelist()
def rename_doc(doctype, name, force=True):
	doc = frappe.get_doc(doctype, name)
	new_name = doc.make_new_name()

	if not new_name == doc.name:

		return frappe.rename_doc(doc.doctype, 
			doc.name, new_name, force=True)
