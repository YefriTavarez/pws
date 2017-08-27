from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Docs"),
			"items": [
				{
					"type": "doctype",
					"name": "Proyecto",
				},
			]
		},
		{
			"label": _("Otros"),
			"items": [
				{
					"type": "doctype",
					"name": "Tarea",
				},
				{
					"type": "doctype",
					"name": "Plantilla de Proyecto",
				},
				{
					"type": "doctype",
					"name": "Tipo de Proyecto",
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
	]
	