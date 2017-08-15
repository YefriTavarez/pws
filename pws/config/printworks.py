from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Docs"),
			"items": [
				{
					"type": "doctype",
					"name": "Perfilador de Productos",
				},
				{
					"type": "doctype",
					"name": "Ensamblador de Productos",
				},
			]
		},
		{
			"label": _("Otros"),
			"items": [
				{
					"type": "doctype",
					"name": "Dimension",
				},
				{
					"type": "doctype",
					"name": "Material de Impresion",
				},
				{
					"type": "doctype",
					"name": "Tecnologia de Impresion",
				}
			]
		},
		{
			"label": _("Integraciones"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
				},
				{
					"type": "doctype",
					"name": "Item Group",
				},
			]
		},
		{
			"label": _("Opciones"),
			"items": [
				{
					"type": "doctype",
					"name": "Opciones de Control",
				},
				{
					"type": "doctype",
					"name": "Opciones de Corte",
				},
				{
					"type": "doctype",
					"name": "Opciones de Empalme",
				},
				{
					"type": "doctype",
					"name": "Opciones de Impresion",
				},
				{
					"type": "doctype",
					"name": "Opciones de Proteccion",
				},
				{
					"type": "doctype",
					"name": "Opciones de Utilidad",
				},
				{
					"type": "doctype",
					"name": "Opciones de Textura",
				},
			]
		},
	]
	