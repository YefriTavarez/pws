# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe
import pws.utils

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
