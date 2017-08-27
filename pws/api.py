# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe
import pws.utils

from frappe.model.naming import make_autoname as autoname

def s_sanitize(string):
	"""Remove the most common special caracters"""

	s_sanitized = string


def s_strip(string):
	"""Clean and convert a string into a valid variable name"""

	# remove blank spaces
	s_word = string.replace(" ", "")

	# convert to lower case
	s_lower = s_word.lower()
	
	# remove most common special caracters
	s_sanitized = s_sanitize(s_lower)

	# convert to upper case
	s_upper = s_sanitized.upper()

	return s_upper

def s_hash(string):
	return pws.utils.s_hash(string)

def gut(string, size=2):
	return [ word[:size]
		for part in string.split("-") 
		for word in part.split()
	]

def project_autoname(project, event):
	name_sanitized = s_sanitize(project.project_name)

	first_two = gut(name_sanitized, size=3)

	naming_serie = "{0}-.#####".format(*first_two)

	project.name = autoname(naming_serie)

	# project.db_update()

def assign_to(doc, event):
	from frappe.desk.form.assign_to import add as assign

	if doc.user:
		assign({
			"assign_to": doc.user,
			"doctype": doc.doctype,
			"name": doc.name,
			"description": doc.subject
		})
