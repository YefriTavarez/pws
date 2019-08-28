# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

import frappe

conf = frappe._dict({
	"item_group": frappe.db.get_single_value("Configuracion General", "item_group"),
	"materials_item_group": frappe.db.get_single_value("Configuracion General", "materials_item_group")
	})

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
	WHERE perfilador.name = %s 
		AND material.name = %s
		AND opt_items.opciones_de_control like %s """,
	(filters.get("perfilador"), filters.get("material"), 
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
		WHERE perfilador.name = %s 
			AND material.name = %s
			AND opt_items.opciones_de_corte like %s """,
		(filters.get("perfilador"), filters.get("material"), 
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
		WHERE perfilador.name = %s 
			AND material.name = %s
			AND opt_items.opciones_de_empalme like %s """,
		(filters.get("perfilador"), filters.get("material"), 
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
		WHERE perfilador.name = %s 
			AND material.name = %s
			AND opt_items.opciones_de_plegado like %s """,
		(filters.get("perfilador"), filters.get("material"), 
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
		WHERE perfilador.name = %s 
			AND material.name = %s
			AND opt_items.opciones_de_proteccion like %s """,
		(filters.get("perfilador"), filters.get("material"), 
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
		WHERE perfilador.name = %s 
			AND material.name = %s
			AND opt_items.opciones_de_utilidad like %s """,
		(filters.get("perfilador"), filters.get("material"), 
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
		WHERE perfilador.name = %s 
			AND material.name = %s
			AND opt_items.opciones_de_textura like %s """,
		(filters.get("perfilador"), filters.get("material"), 
			"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.opciones_de_textura] for row in textura_list]

def ens_dimension_query(doctype, txt, searchfield, start, page_len, filters):
	dimension_list = frappe.get_list("Perfilador de Productos Items", {
		"products": filters.get("perfilador"),
		"parent": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["parent"], order_by="parent")
	
	return [[row.parent] for row in dimension_list]

def item_manufactured_query(doctype, txt, searchfield, start, page_len, filters):

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
		""".format(conf.item_group, txt))

	return item_list

def project_template_query(doctype, txt, searchfield, start, page_len, filters):
	template_list = frappe.get_list("Plantilla de Proyecto", {
		"enabled": "1",
		"name": ["like", "%{}%".format(txt) if txt else "%"]
	}, ["name"], order_by="name")

	return [[row.name] for row in template_list]

def item_query(doctype, txt, searchfield, start, page_len, filters):
	item_list = frappe.db.sql("""SELECT
			`tabItem`.name,
			`tabItem`.description
		FROM tabItem
		WHERE disabled = 0
			AND (description LIKE %s
			OR name LIKE %s)
		ORDER BY name ASC""", ("%{0}%".format(txt) if txt else "%", 
		"%{0}%".format(txt) if txt else "%"), as_dict=True, debug=False)

	return [[row.name, row.description] for row in item_list]

def project_customer(doctype, txt, searchfield, start, page_len, filters):
	txt = "%".join(txt.split())

	customer_list = frappe.get_list("Proyecto", {
		"title": ["like", "%{}%".format(txt) if txt else "%"],
		"status": filters.get("status"),
	}, ["distinct customer"], order_by="customer")

	return [[row.customer] for row in customer_list]

def project_item(doctype, txt, searchfield, start, page_len, filters):
	txt = "%".join(txt.split())

	item_list = frappe.get_list("Proyecto", {
		"title": ["like", "%{}%".format(txt) if txt else "%"],
		"customer": filters.get("customer")
	}, ["distinct item", "item_name"], order_by="customer")

	return [[row.item, row.item_name] for row in item_list]

def ordered_item_group_query(doctype, txt, searchfield, start, page_len, filters):
	txt = txt and "%".join(txt.split())

	item_group_list = frappe.db.sql("""SELECT
			name, item_group_code 
		FROM
			`tabItem Group` 
		WHERE
			parent_item_group = %s 
			AND name LIKE %s 
		ORDER BY
			name""", (filters.get("parent_item_group"), "%{}%".format(txt) if txt else "%"),
	as_dict=True)

	return [[row.name] for row in item_group_list]

def attach_type_query(doctype, txt, searchfield, start, page_len, filters):
	txt = "%".join(txt.split())

	attach_type_list = frappe.db.sql("""SELECT 
			attach_type, abbr
		FROM `tabTipo de Adjunto`
		WHERE enabled = 1
			AND (attach_type LIKE %s OR abbr LIKE %s)
		ORDER BY attach_type
		""", ("%{}%".format(txt) if txt else "%",
	"%{}%".format(txt) if txt else "%"), as_dict=True)

	return [[row.attach_type, row.abbr] for row in attach_type_list]

def tarea_por_usuario_report_query(doctype, txt, searchfield, start, page_len, filters):
	txt = "%".join(txt.split())

	result = frappe.db.sql("""SELECT DISTINCT
			parent
		FROM
			`tabHas Role` 
		WHERE
			parenttype = "USER" 
			AND role = "Usuario de Proyectos" 
			AND parent != "Administrator"
			AND parent LIKE %s 
		""", "%{}%".format(txt) if txt else "%", 
	as_dict=True)

	return [frappe.get_value("User", user.parent, ["name", "full_name"]) for user in result]

def project_manager_query(doctype, txt, searchfield, start, page_len, filters):
	txt = "%".join(txt.split())

	result = frappe.db.sql("""SELECT DISTINCT
			parent
		FROM
			`tabHas Role` 
		WHERE
			parenttype = "USER" 
			AND role = "Supervisor de Proyectos" 
			AND parent != "Administrator"
			AND parent LIKE %s 
		""", "%{}%".format(txt) if txt else "%", 
	as_dict=True)

	return [frappe.get_value("User", user.parent, ["name", "full_name"]) for user in result]

def project_user_query(doctype, txt, searchfield, start, page_len, filters):
	txt = "%".join(txt.split())

	result = frappe.db.sql("""SELECT DISTINCT
			parent
		FROM
			`tabHas Role` 
		WHERE
			parenttype = "User" 
			AND role = "Usuario de Proyectos" 
			AND parent != "Administrator"
			AND parent LIKE %s 
		""", "%{}%".format(txt) if txt else "%", 
	as_dict=True)

	return [frappe.get_value("User", user.parent, ["name", "full_name"]) for user in result]

def user_query(doctype, txt, searchfield, start, page_len, filters):
	filters.update({
		"txt": "%{}%".format(txt) if txt else "%"
	})

	result = frappe.db.sql("""SELECT DISTINCT
			parent
		FROM
			`tabHas Role` 
		WHERE
			parenttype = "User" 
			AND role = %(role)s 
			AND parent != "Administrator"
			AND parent LIKE %(txt)s 
		""", filters, 
	as_dict=True)

	return [frappe.get_value("User", user.parent, ["name", "full_name"]) for user in result]

def doctype_query(doctype, txt, searchfield, start, page_len, filters):
	item_list = frappe.get_all("DocType", {
		"name": ["in", "Customer, Supplier, Employee, Other"],
	}, ["distinct name"], order_by="name")

	return [[row.name] for row in item_list]