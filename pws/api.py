# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe
import pws.utils

from frappe.utils import flt

def s_sanitize(string):
	"""Remove the most common special caracters"""

	special_cars = [
		(u"á", "a"), (u"Á", "A"),
		(u"é", "e"), (u"É", "E"),
		(u"í", "i"), (u"Í", "I"),
		(u"ó", "o"), (u"Ó", "O"),
		(u"ú", "u"), (u"Ú", "U"),
		(u"ü", "u"), (u"Ü", "U"),
		(u"ñ", "n"), (u"Ñ", "N")
	]

	s_sanitized = string

	for pair in special_cars:
		s_sanitized = s_sanitized.replace(pair[0], pair[1])

	return s_sanitized.upper()

def s_strip(string):
	"""Clean and convert a string into a valid variable name"""

	# remove blank spaces
	s_word = string.replace(" ", "")

	# remove most common special caracters
	s_sanitized = s_sanitize(s_word)

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

def get_materials_item_group():
	material_item_group = frappe.get_value("Item Group", {
		"name": "Material de Impresion"
	}, ["name"])

	if material_item_group:
		return material_item_group

	item_group = frappe.new_doc("Item Group")
	item_group.update({
		"parent_item_group": "All Item Groups",
		"item_group_name": "Material de Impresion",
		"route": "materiales/material-de-impresion"
	})

	item_group.save()

	return item_group.get("name")

def add_to_date(date, years=0, months=0, days=0, hours=0, minutes=0, as_string=False, as_datetime=False):
	"""Adds `days` to the given date"""
	from dateutil import  parser
	from dateutil.relativedelta import relativedelta

	if date == None:
		date = frappe.utils.now_datetime()

	if hours:
		as_datetime = True

	if isinstance(date, basestring):
		as_string = True

		if " " in date:
			as_datetime = True

		date = parser.parse(date)

	date = date + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes)

	if as_string:
		if as_datetime:
			return date.strftime(frappe.utils.DATETIME_FORMAT)
		else:
			return date.strftime(frappe.utils.DATE_FORMAT)
	else:
		return date

def item_autoname(doc, event):
	item_validate(doc, event)

	if doc.item_group == "All Item Groups":
		name = "00000000"

		length = len(frappe.get_list("Item", { "item_group": doc.item_group }))
		code = int(length) # convert it to int

		item_group_code = "{0:04d}".format(code + 1)

		doc.name = "{0}{1}".format(name, item_group_code)

		return False

	parent_codes = get_parent_code(doc.item_group, [])

	parents_code = "".join(parent_codes)

	array = [c for c in parents_code]

	length = len(frappe.get_list("Item", { "item_group": doc.item_group }))
	code = int(length) # convert it to int

	item_group_code = "{0:04d}".format(code + 1)

	missing_length = 8 - len(array)

	for e in range(missing_length):
		array.append("0")

	array += item_group_code

	doc.name = "".join(array)

def item_validate(doc, event):
	doc.item_group = doc.item_group_4 or doc.item_group_3\
		or doc.item_group_2 or doc.item_group_1

def item_ontrash(doc, event):

	id = doc.name

	length = len(frappe.get_list("Item", {
		"item_group": doc.item_group
	}))

	current_value = flt(id[-4:])

	if current_value < length:
		frappe.throw("""No puede eliminar este articulo porque no fue el 
				ultimo creado debajo de esta categoria""")

def item_group_update(doc, event):
	if not doc.item_group_name == "All Item Groups":
		latest = get_lastest_code(doc.parent_item_group)

		code = int(latest) # convert it to int

		doc.item_group_code = "{0:02d}".format(code + 1)

	doc.db_update()

def get_lastest_code(parent):
	r = frappe.db.sql("""SELECT IFNULL(MAX(item_group_code), 0)
		FROM `tabItem Group`
		WHERE parent_item_group = '%s'""" % parent, as_list=True)

	return r and r[0][0]

def get_parent_code(item_group, array=[]):
    doc = frappe.get_doc("Item Group", item_group)
    
    array.append(doc.item_group_code)

    if doc.parent_item_group == "All Item Groups":
    	
    	iterator = reversed(array)

        return list(iterator)

    return get_parent_code(doc.parent_item_group, array)

def on_session_creation():
	# frappe.msgprint("Bienvenido {}".format(frappe.session.user))

	msg = "User {} has been logged in!".format(frappe.session.user)
	frappe.publish_realtime(event='msgprint', message=msg, user='yefritavarez@gmail.com') 