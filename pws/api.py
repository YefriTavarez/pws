# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe
import pws.utils

from frappe.utils import flt

from pws.solicitudes.doctype.solicitud_de_pago import solicitud_de_pago

def s_sanitize(string, upper=True):
	"""Remove the most common special caracters"""

	special_cars = [
		(u"á", "a"), (u"Á", "A"),
		(u"é", "e"), (u"É", "E"),
		(u"í", "i"), (u"Í", "I"),
		(u"ó́", "o"), (u"Ó", "O"),
		(u"ó", "o"), (u"Ó", "O"),
		(u"ú", "u"), (u"Ú", "U"),
		(u"ü", "u"), (u"Ü", "U"),
		(u"ñ", "n"), (u"Ñ", "N")
	]

	s_sanitized = string

	for pair in special_cars:
		s_sanitized = s_sanitized.replace(pair[0], pair[1])

	if upper:
		return s_sanitized.upper()

	import re
	s_sanitized = re.sub('[^a-zA-Z0-9\n\./,()\-]', ' ', s_sanitized)

	return s_sanitized


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
	return frappe.db.get_single_value("Configuracion General", "materials_item_group")

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

def item_group_autoname(doc, event):

	if not doc.item_group_name == "All Item Groups":
		latest = get_lastest_code(doc.parent_item_group)

		code = int(latest) # convert it to int

		doc.item_group_code = "{0:02d}".format(code + 1)

	doc.name = "{0} - {1}".format(doc.item_group_code, 
		doc.item_group_name.encode("utf-8").strip())

def get_lastest_code(parent):
	r = frappe.db.sql("""
		SELECT 
			IFNULL(MAX(item_group_code), 0)
		FROM 
			`tabItem Group`
		WHERE 
			parent_item_group = '%s'
	""" % parent, as_list=True)

	return r and r[0][0]

def get_parent_code(item_group, array=[]):
    doc = frappe.get_doc("Item Group", item_group)
    
    array.append(doc.item_group_code)

    if doc.parent_item_group == "All Item Groups":
    	
    	iterator = reversed(array)

        return list(iterator)

    return get_parent_code(doc.parent_item_group, array)

def on_session_creation():
	from frappe.auth import delete_session
	if not frappe.session.user == "yefritavarez@gmail.com" and False: 
		delete_session(frappe.session.sid)
		
		msg = "User {0} has tried to log in at {1}!".format(frappe.session.user, frappe.utils.now_datetime())
		
		frappe.publish_realtime(event='msgprint', message=msg, user='yefritavarez@gmail.com')
		frappe.throw("Estamos trabajando en el sistema. Intente mas tarde!")
	

def showmessage(doc, event):
	frappe.throw("Espere unos minutos antes de volver a intentar guardar esta factura")

@frappe.whitelist()
def make_payment_entry(doctype, name):
	return solicitud_de_pago.make_payment_entry(doctype, name)

@frappe.whitelist()
def make_journal_entry(doctype, name):
	return solicitud_de_pago.make_journal_entry(doctype, name)