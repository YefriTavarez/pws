# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe

def product_type_query(doctype, txt, searchfield, start, page_len, filters):
	item_group_list = frappe.get_list("Item Group", {
		"is_group": "0",
		"parent_item_group": filters.get("category")
	}, order_by="name")

	product_type_list = []
	for item_group in item_group_list:
		_filters = {
			"name": ["like", "%{0}%".format(txt if txt else item_group.name)]
		}

		product_type = frappe.get_value("Perfilador de Productos", _filters, ["name"])

		if product_type:
			product_type_list.append([product_type])

	return sorted(product_type_list)

def ens_materials_query(doctype, txt, searchfield, start, page_len, filters):
	material_list = frappe.get_list("Material de Impresion Items", {
		"parent": filters.get("perfilador"),
		"material_name": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["materials", "material_name"], order_by="materials")

	return [[row.materials, row.material_name] for row in material_list]

def ens_control_query(doctype, txt, searchfield, start, page_len, filters):
	control_list = frappe.get_list("Opciones de Control Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_control": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_control"], order_by="opciones_de_control")

	return [[row.opciones_de_control] for row in control_list]

def ens_corte_query(doctype, txt, searchfield, start, page_len, filters):
	corte_list = frappe.get_list("Opciones de Corte Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_corte": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_corte"], order_by="opciones_de_corte")

	return [[row.opciones_de_corte] for row in corte_list]

def ens_empalme_query(doctype, txt, searchfield, start, page_len, filters):
	empalme_list = frappe.get_list("Opciones de Empalme Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_empalme": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_empalme"], order_by="opciones_de_empalme")

	return [[row.opciones_de_empalme] for row in empalme_list]

def ens_plegado_query(doctype, txt, searchfield, start, page_len, filters):
	plegado_list = frappe.get_list("Opciones de Plegado Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_plegado": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_plegado"], order_by="opciones_de_plegado")

	return [[row.opciones_de_plegado] for row in plegado_list]

def ens_proteccion_query(doctype, txt, searchfield, start, page_len, filters):
	proteccion_list = frappe.get_list("Opciones de Proteccion Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_proteccion": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_proteccion"], order_by="opciones_de_proteccion")

	return [[row.opciones_de_proteccion] for row in proteccion_list]

def ens_utilidad_query(doctype, txt, searchfield, start, page_len, filters):
	utilidad_list = frappe.get_list("Opciones de Utilidad Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_utilidad": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_utilidad"], order_by="opciones_de_utilidad")

	return [[row.opciones_de_utilidad] for row in utilidad_list]

def ens_textura_query(doctype, txt, searchfield, start, page_len, filters):
	textura_list = frappe.get_list("Opciones de Textura Items", {
		"parent": filters.get("perfilador"),
		"opciones_de_textura": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["opciones_de_textura"], order_by="opciones_de_textura")

	return [[row.opciones_de_textura] for row in textura_list]

def ens_dimension_query(doctype, txt, searchfield, start, page_len, filters):
	dimension_list = frappe.get_list("Perfilador de Productos Items", {
		"products": filters.get("perfilador"),
		"parent": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["parent"], order_by="parent")
	
	return [[row.parent] for row in dimension_list]

def item_manufactured_query(doctype, txt, searchfield, start, page_len, filters):
	default_item_group = frappe.db.get_single_value("Configuracion General", "item_group")

	item_list = frappe.db.sql("""SELECT item.name, item.description 
		FROM `tabItem` AS item 
		JOIN `tabItem Group` AS item_group 
			ON item_group.name = item.item_group 
		WHERE item_group.parent_item_group = '{0}'
			AND (
					item.name LIKE '%{1}%'
				OR 
					item.description LIKE '%{1}%'
				)
		""".format(default_item_group, txt))

	return item_list

def project_template_query(doctype, txt, searchfield, start, page_len, filters):
	template_list = frappe.get_list("Plantilla de Proyecto", {
		"enabled": "1",
		"name": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["name"], order_by="name")

	return [[row.name] for row in template_list]
