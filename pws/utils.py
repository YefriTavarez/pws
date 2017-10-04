# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe
import hashlib

def s_hash(string):
	h = hashlib.sha1(string)

	return h.hexdigest()

def disable_projects_from_erpnext():
	doclist = [
		"5710c980ae", "1da642d61a",
		"b77cedf6de", "f7ee96e8bd",
		"54e6d52b6b", "bede1f5e90",
		"ceaf17d037", "0765d635b2",
		"912d00cdc0", "ae029e1fe9",
		"284aaa3a0f", "1b8ad04da8",
		"2ae371df88", "2bb0a14d3f",
		"66f66db17c", "8a14147911",
		"b6302eb757"
	]

	for docperm in doclist:
		frappe.delete_doc_if_exists("DocPerm", docperm)

	change_from_project_to_proyecto()

def change_from_project_to_proyecto():

	for fieldname in frappe.get_list("DocField", {"fieldtype": "Link", "options": "Project" }):
		doc = frappe.get_doc("DocField", fieldname.name)
		doc.options = "Proyecto"
		doc.db_update()

