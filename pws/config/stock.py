from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Items and Pricing"),
			"items": [
				{
					"type": "doctype",
					"name": "Perfilador de Productos",
				},
				{
					"type": "doctype",
					"name": "Ensamblador de Productos",
				},
				{
					"type": "doctype",
					"name": "Material de Impresion",
				},
			]
		},
		{
			"label": _("Opciones de Productos"),
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
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Dimensiones",
				},
				{
					"type": "doctype",
					"name": "Tecnologia de Impresion",
				},
			]
		}
	]
	