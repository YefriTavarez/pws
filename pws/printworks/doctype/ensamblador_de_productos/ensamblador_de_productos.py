# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EnsambladordeProductos(Document):
	def autoname(self):
		array = []

		fields = [
			self.perfilador_de_productos,
			self.materials,
			self.opciones_de_control,
			self.opciones_de_corte,
			self.opciones_de_empalme,
			self.opciones_de_plegado,
			self.opciones_de_proteccion,
			self.opciones_de_utilidad,
			self.opciones_de_textura
		]

		for key in fields:
			if key:
				array += gut(key)

		new_name = "".join(array).upper()

		exists = frappe.get_value("Ensamblador de Productos", new_name)

		if exists:
			frappe.throw("""Ensamblador 
				<a href='/desk#Form/Ensamblador de Productos/{0}'>{0}</a> ya existe.""".format(
					new_name))

		self.name = new_name

def gut(string):
	return [ choose(word)
		for part in string.split("-") 
		for word in part.split()
	]

def choose(value):
	return value if value.isdigit() else value[0]