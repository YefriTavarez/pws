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
	control_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_control
	FROM `tabOpciones de Control Items` AS opt_items 
		JOIN `tabPerfilador de Productos` AS perfilador 
			ON perfilador.name = opt_items.parent 
		JOIN `tabOpciones de Control` AS opt 
			ON opt.name = opt_items.opciones_de_control 
		JOIN `tabTecnologia Items` AS tecnologia_opts 
			ON tecnologia_opts.parent = opt.name 
		JOIN `tabTecnologia Items` AS tecnologia_material 
			ON tecnologia_opts.technology = tecnologia_material.technology 
		JOIN `tabMaterial de Impresion` AS material 
			ON material.name = tecnologia_material.parent 
	WHERE perfilador.name = '{0}' 
		AND material.name = '{1}'
		AND opt_items.opciones_de_control like '{2}' """
	.format(filters.get("perfilador"), filters.get("material"), 
		"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_control] for row in control_list]

def ens_corte_query(doctype, txt, searchfield, start, page_len, filters):
	corte_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_corte
		FROM `tabOpciones de Corte Items` AS opt_items 
			JOIN `tabPerfilador de Productos` AS perfilador 
				ON perfilador.name = opt_items.parent 
			JOIN `tabOpciones de Corte` AS opt 
				ON opt.name = opt_items.opciones_de_corte 
			JOIN `tabTecnologia Items` AS tecnologia_opts 
				ON tecnologia_opts.parent = opt.name 
			JOIN `tabTecnologia Items` AS tecnologia_material 
				ON tecnologia_opts.technology = tecnologia_material.technology 
			JOIN `tabMaterial de Impresion` AS material 
				ON material.name = tecnologia_material.parent 
		WHERE perfilador.name = '{0}' 
			AND material.name = '{1}'
			AND opt_items.opciones_de_corte like '{2}' """
		.format(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_corte] for row in corte_list]

def ens_empalme_query(doctype, txt, searchfield, start, page_len, filters):
	empalme_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_empalme
		FROM `tabOpciones de Empalme Items` AS opt_items 
			JOIN `tabPerfilador de Productos` AS perfilador 
				ON perfilador.name = opt_items.parent 
			JOIN `tabOpciones de Empalme` AS opt 
				ON opt.name = opt_items.opciones_de_empalme 
			JOIN `tabTecnologia Items` AS tecnologia_opts 
				ON tecnologia_opts.parent = opt.name 
			JOIN `tabTecnologia Items` AS tecnologia_material 
				ON tecnologia_opts.technology = tecnologia_material.technology 
			JOIN `tabMaterial de Impresion` AS material 
				ON material.name = tecnologia_material.parent 
		WHERE perfilador.name = '{0}' 
			AND material.name = '{1}'
			AND opt_items.opciones_de_empalme like '{2}' """
		.format(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_empalme] for row in empalme_list]

def ens_plegado_query(doctype, txt, searchfield, start, page_len, filters):
	plegado_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_plegado
		FROM `tabOpciones de Plegado Items` AS opt_items 
			JOIN `tabPerfilador de Productos` AS perfilador 
				ON perfilador.name = opt_items.parent 
			JOIN `tabOpciones de Plegado` AS opt 
				ON opt.name = opt_items.opciones_de_plegado 
			JOIN `tabTecnologia Items` AS tecnologia_opts 
				ON tecnologia_opts.parent = opt.name 
			JOIN `tabTecnologia Items` AS tecnologia_material 
				ON tecnologia_opts.technology = tecnologia_material.technology 
			JOIN `tabMaterial de Impresion` AS material 
				ON material.name = tecnologia_material.parent 
		WHERE perfilador.name = '{0}' 
			AND material.name = '{1}'
			AND opt_items.opciones_de_plegado like '{2}' """
		.format(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_plegado] for row in plegado_list]

def ens_proteccion_query(doctype, txt, searchfield, start, page_len, filters):
	proteccion_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_proteccion
		FROM `tabOpciones de Proteccion Items` AS opt_items 
			JOIN `tabPerfilador de Productos` AS perfilador 
				ON perfilador.name = opt_items.parent 
			JOIN `tabOpciones de Proteccion` AS opt 
				ON opt.name = opt_items.opciones_de_proteccion 
			JOIN `tabTecnologia Items` AS tecnologia_opts 
				ON tecnologia_opts.parent = opt.name 
			JOIN `tabTecnologia Items` AS tecnologia_material 
				ON tecnologia_opts.technology = tecnologia_material.technology 
			JOIN `tabMaterial de Impresion` AS material 
				ON material.name = tecnologia_material.parent 
		WHERE perfilador.name = '{0}' 
			AND material.name = '{1}'
			AND opt_items.opciones_de_proteccion like '{2}' """
		.format(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_proteccion] for row in proteccion_list]

def ens_utilidad_query(doctype, txt, searchfield, start, page_len, filters):
	utilidad_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_utilidad
		FROM `tabOpciones de Utilidad Items` AS opt_items 
			JOIN `tabPerfilador de Productos` AS perfilador 
				ON perfilador.name = opt_items.parent 
			JOIN `tabOpciones de Utilidad` AS opt 
				ON opt.name = opt_items.opciones_de_utilidad 
			JOIN `tabTecnologia Items` AS tecnologia_opts 
				ON tecnologia_opts.parent = opt.name 
			JOIN `tabTecnologia Items` AS tecnologia_material 
				ON tecnologia_opts.technology = tecnologia_material.technology 
			JOIN `tabMaterial de Impresion` AS material 
				ON material.name = tecnologia_material.parent 
		WHERE perfilador.name = '{0}' 
			AND material.name = '{1}'
			AND opt_items.opciones_de_utilidad like '{2}' """
		.format(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_utilidad] for row in utilidad_list]

def ens_textura_query(doctype, txt, searchfield, start, page_len, filters):
	textura_list = frappe.db.sql("""SELECT DISTINCT opt_items.opciones_de_textura
		FROM `tabOpciones de Textura Items` AS opt_items 
			JOIN `tabPerfilador de Productos` AS perfilador 
				ON perfilador.name = opt_items.parent 
			JOIN `tabOpciones de Textura` AS opt 
				ON opt.name = opt_items.opciones_de_textura 
			JOIN `tabTecnologia Items` AS tecnologia_opts 
				ON tecnologia_opts.parent = opt.name 
			JOIN `tabTecnologia Items` AS tecnologia_material 
				ON tecnologia_opts.technology = tecnologia_material.technology 
			JOIN `tabMaterial de Impresion` AS material 
				ON material.name = tecnologia_material.parent 
		WHERE perfilador.name = '{0}' 
			AND material.name = '{1}'
			AND opt_items.opciones_de_textura like '{2}' """
		.format(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

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
