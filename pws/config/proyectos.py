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
					"label": "Proyectos"
				},
				{
					"type": "doctype",
					"name": "Tarea",
					"label": "Tareas"
				},
				{
					"type": "doctype",
					"name": "Plantilla de Proyecto",
					"label": "Plantilla de Proyectos"
				},
			]
		},
		{
			"label": _("Otros"),
			"items": [
				{
					"type": "doctype",
					"name": "Tipo de Proyecto",
					"label": "Tipo de Proyectos",
				},
				{
					"type": "doctype",
					"name": "Tipo de Adjunto",
					"label": "Tipo de Adjuntos",
				},

			]
		},
	]
	