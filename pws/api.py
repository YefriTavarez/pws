import frappe

def product_type_query(doctype, txt, searchfield, start, page_len, filters):
	item_group_list = frappe.get_list("Item Group", {
		"is_group": "0",
		"parent_item_group": filters.get("category")
	})

	product_type_list = []
	for item_group in item_group_list:
		_filters = {
			"name": ["like", "%{0}%".format(txt if txt else item_group.name)]
		}

		product_type = frappe.get_value("Perfilador de Productos", _filters, ["name"])

		if product_type:
			product_type_list.append([product_type])

	return product_type_list

def ens_materials_query(doctype, txt, searchfield, start, page_len, filters):
	material_list = frappe.get_list("Material de Impresion Items", {
		"parent": filters.get("perfilador")
	}, ["materials"])

	return [[row.materials] for row in material_list]

def ens_control_query(doctype, txt, searchfield, start, page_len, filters):
	control_list = frappe.get_list("Opciones de Control Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_control"])

	return [[row.opciones_de_control] for row in control_list]

def ens_corte_query(doctype, txt, searchfield, start, page_len, filters):
	corte_list = frappe.get_list("Opciones de Corte Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_corte"])

	return [[row.opciones_de_corte] for row in corte_list]

def ens_empalme_query(doctype, txt, searchfield, start, page_len, filters):
	empalme_list = frappe.get_list("Opciones de Empalme Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_empalme"])

	return [[row.opciones_de_empalme] for row in empalme_list]

def ens_plegado_query(doctype, txt, searchfield, start, page_len, filters):
	plegado_list = frappe.get_list("Opciones de Plegado Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_plegado"])

	return [[row.opciones_de_plegado] for row in plegado_list]

def ens_proteccion_query(doctype, txt, searchfield, start, page_len, filters):
	proteccion_list = frappe.get_list("Opciones de Proteccion Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_proteccion"])

	return [[row.opciones_de_proteccion] for row in proteccion_list]

def ens_utilidad_query(doctype, txt, searchfield, start, page_len, filters):
	utilidad_list = frappe.get_list("Opciones de Utilidad Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_utilidad"])

	return [[row.opciones_de_utilidad] for row in utilidad_list]

def ens_textura_query(doctype, txt, searchfield, start, page_len, filters):
	textura_list = frappe.get_list("Opciones de Textura Items", {
		"parent": filters.get("perfilador")
	}, ["opciones_de_textura"])

	return [[row.opciones_de_textura] for row in textura_list]
