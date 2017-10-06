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
	def autoname(self):
		self.validate()
		self.name = self.new_name

	def validate(self):
		new_hash = self.make_new_hash()

		self.hash = new_hash.upper()

		self.after_validate()

	def after_validate(self):
		number_fields = [
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro"
		]

		for field in number_fields:
			self.set(field, int(self.get(field)))

		self.create_item()

	def make_new_hash(self):
		array = ["".join(
			gut(self.get(key)))
			for key in self.get_fields() 
		if str(self.get(str(key)))] 

		pre_hash = "".join(array).upper()
		frappe.errprint("pre_hash {}".format(pre_hash))

		pre_hash_with_textures = "{0}{1}".format(pre_hash,
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

	def get_textura_names(self):
		array = ""

		for textura in self.opciones_de_textura:
			array += "".join(
				gut(textura.opciones_de_textura))

		return "".join(array)

	def get_utility_names(self):
		array = ""

		for utilidad in self.opciones_de_utilidad:
			array += "".join(
				gut(utilidad.opciones_de_utilidad))

		return "".join(array)

	def get_fields(self):
		return [
			"perfilador_de_productos",
			"materials_title",
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro",
			"dimension",
			"opciones_de_control",
			"opciones_de_empalme",
			"opciones_de_plegado",
			"opciones_de_proteccion",
			"opciones_de_corte",
		]

	def create_item(self):
		# new item allocated
		item = frappe.new_doc("Item")

		# from the bottom to the top choose the first one with value
		item_group = self.item_group_4 or self.item_group_3 or self.item_group_2 or self.item_group_1

		# load configuration from the control panel
		products_are_stock_items = frappe.db.get_single_value("Configuracion General", 
			"products_are_stock_items")

		item_name = "{0} {1} {2}".format(self.perfilador_de_productos, self.materials_title, self.dimension)

		# if the item exists
		if frappe.get_value("Item", { "hash": self.hash }):
			# let's load it and use it
			item = frappe.get_doc("Item", { "hash": self.hash })

		description = self.get_self_description()

		for utilidad in self.opciones_de_utilidad:
			description ="{0}, {1}".format(description, " ".join(
				gut(utilidad.opciones_de_utilidad)))

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
		self.new_name = item.name

	def get_self_description(self):
		description = ", ".join([self.get_label(field)
			for field in self.get_fields() 
			if self.get(field)])

		new_desc =  description.replace("Tiro,   +", "+")\
			.replace("Retiro,   +", "+")
			
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
			"cantidad_tiro_pantone": "+ {0} {1} Pantone Tiro".format(self.get(field), color_o_colores),
			"cantidad_proceso_retiro": "{0} {1} Proceso Retiro".format(self.get(field), color_o_colores) if not flt(self.get(field)) > 3.000 else "Full Color Pantone Retiro",
			"cantidad_pantone_retiro": "+ {0} {1} Pantone Retiro".format(self.get(field), color_o_colores)
		}

		if d.get(field):
			return " {}".format(d.get(field))

		return field

def gut(string):
	string = str(string)
	return [ word
		for part in string.split("-") 
		for word in part.split()
	]
