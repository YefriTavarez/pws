# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import pws.api

from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt

class EnsambladordeProductos(Document):
	prev_field = 0
	def before_insert(self):
		# fields that are integers but are rendered
		# as dropdown lists and hence treated as string 
		# are coverted to integer
		number_fields = [
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro"
		]

		# here's where magic is happening
		for field in number_fields:
			self.set(field, int(self.get(field)))

		self.create_or_update_item(create=True)

	def autoname(self):
		# this is where the name is set
		self.name = self.new_name

	def validate(self):

		# generate a new hash for helping to identify
		# the sku (an Item in ERPNext)
		new_hash = self.make_new_hash()

		self.hash = new_hash.upper()

		self.update_item()

	def update_item(self):
		# fields that are integers but are rendered
		# as dropdown lists and hence treated as string 
		# are coverted to integer
		number_fields = [
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro"
		]

		# here's where magic is happening
		for field in number_fields:
			self.set(field, int(self.get(field)))

		self.create_or_update_item(create=False)

	def make_new_hash(self):
		array = ["".join(
			gut(self.get(key)))
			for key in self.get_fields() 
		if (self.get(key) if isinstance(self.get(key), basestring) else str(self.get(key)))] 

		pre_hash = "".join(array).upper()

		pre_hash_with_proteccions = "{0}{1}".format(pre_hash,
			self.get_proteccion_names())

		pre_hash_with_textures = "{0}{1}".format(pre_hash_with_proteccions,
			self.get_textura_names())

		pre_hash_with_utilities = "{0}{1}".format(pre_hash_with_textures,
			self.get_utility_names())

		new_hash = pws.api.s_sanitize(
			u"{0}".format(pre_hash_with_utilities))

		exists = frappe.get_value("Ensamblador de Productos", {
			"hash": new_hash.upper()
		}, ["name"])

		if exists and not exists == self.name and not new_hash.upper() == self.hash:
			frappe.throw("""Ensamblador <a href='/desk#Form/Ensamblador de Productos/{0}'>{0}</a> ya existe con las mismas
				especificaciones.""".format(exists))

		return new_hash

	def get_proteccion_names(self):
		protecciones = ""

		for proteccion in sorted([opt.opciones_de_proteccion for opt in self.opciones_de_proteccion]):
			protecciones = "{0}{1}".format(protecciones, "".join(gut(proteccion)))

		return "".join(protecciones)

	def get_textura_names(self):
		texturas = ""

		for textura in sorted([opt.opciones_de_textura for opt in self.opciones_de_textura]):
			texturas = "{0}{1}".format(texturas, "".join(gut(textura)))

		return texturas

	def get_utility_names(self):
		utilidades = ""

		for utilidad in sorted([opt.opciones_de_utilidad for opt in self.opciones_de_utilidad]):
			utilidades = "{0}{1}".format(utilidades, "".join(gut(utilidad)))

		return utilidades

	def get_fields(self):
		return [
			"perfilador_de_productos",
			"materials_title",
			"dimension",
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro",
			"opciones_de_control",
			"opciones_de_plegado",
			"opciones_de_corte",
			"opciones_de_empalme",
		]

	def get_description_fields(self):
		protecciones_list = []
		utilidades_list = []
		texturas_list = []

		for proteccion in self.opciones_de_proteccion:
			protecciones_list.append(" ".join(gut(proteccion.opciones_de_proteccion)))

		for textura in self.opciones_de_textura:
			texturas_list.append(" ".join(gut(textura.opciones_de_textura)))

		for utilidad in self.opciones_de_utilidad:
			utilidades_list.append(" ".join(gut(utilidad.opciones_de_utilidad)))

		self.protecciones = ", ".join(protecciones_list)
		self.utilidades = ", ".join(utilidades_list)
		self.texturas = ", ".join(texturas_list)

		return [
			"perfilador_de_productos",
			"materials_title",
			"dimension",
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro",
			"opciones_de_control",
			"protecciones",
			"texturas",
			"opciones_de_corte",
			"opciones_de_plegado",
			"opciones_de_empalme",
			"utilidades"
		]

	def create_or_update_item(self, create=False):
		# new item allocated

		item = create and frappe.new_doc("Item")

		# from the bottom to the top choose the first one with value
		item_group = self.item_group_4 or self.item_group_3 or self.item_group_2 or self.item_group_1

		# load configuration from the control panel
		products_are_stock_items = frappe.db.get_single_value("Configuracion General", 
			"products_are_stock_items")

		item_name = "{0}, {1}, {2}".format(self.perfilador_de_productos, self.materials_title, self.dimension)

		# if the item exists
		if frappe.get_value("Item", { "name": self.item }):
			# let's load it and use it
			item = frappe.get_doc("Item", { "name": self.item })


		description = self.get_self_description()

		item.update({
			"item_code": item_name,
			"hash": self.hash,
			"item_name": item_name,
			"item_group_1": self.item_group_1,
			"item_group_2": self.item_group_2,
			"item_group_3": self.item_group_3,
			"item_group_4": self.item_group_4,
			"item_group": item_group,
			"description": "{}.".format(description),
			"is_stock_item": products_are_stock_items,
			"is_purchase_item": "0",
			"is_sales_item": "1"
		})

		item.save()

		# update refs
		self.new_name = item.name
		self.item = item.name

	def get_self_description(self):
		description = ", ".join([self.get_label(field)
			for field in self.get_description_fields() 
			if self.get(field)])

		new_desc =  description.replace("Tiro,   +", "+")\
			.replace("Retiro,   +", "+")
			
		self.prev_field = 0
		return new_desc

	def on_trash(self):
		frappe.delete_doc_if_exists("Item", self.name)

	def get_label(self, field):
		if not field in ["cantidad_tiro_proceso", "cantidad_tiro_pantone",
			"cantidad_proceso_retiro", "cantidad_pantone_retiro"]:
			return self.get(field)

		plural = flt(self.get(field)) > 1.000

		color_o_colores = "Colores" if plural else "Color"

		d = {
			"cantidad_tiro_proceso": "{0} {1} Proceso Tiro".format(self.get(field), color_o_colores) if not flt(self.get(field)) > 3.000 else "Full Color Tiro",
			"cantidad_tiro_pantone": "{0} {1} Pantone Tiro".format("+ %s" % self.get(field) if self.prev_field and flt(self.get(self.prev_field)) else self.get(field), color_o_colores),
			"cantidad_proceso_retiro": "{0} {1} Proceso Retiro".format(self.get(field), color_o_colores) if not flt(self.get(field)) > 3.000 else "Full Color Retiro",
			"cantidad_pantone_retiro": "{0} {1} Pantone Retiro".format("+ %s" % self.get(field) if self.prev_field and flt(self.get(self.prev_field)) else self.get(field), color_o_colores)
		}

		self.prev_field = self.get(field)
		if d.get(field):
			return " {}".format(d.get(field))

		return field

def gut(string):
	string = string if isinstance(string, basestring) else str(string)
	return [ word
		for part in string.split("-") 
		for word in part.split()
	]
