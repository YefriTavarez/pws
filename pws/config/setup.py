from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Data"),
			"items": [
				{
					"type": "doctype",
					"name": "Tipo de Adjunto",
					"label": "Tipo de Adjuntos",
				},
			]
		},
		{
			"label": _("Stock"),
			"items": [
				{
					"type": "doctype",
					"name": "Configuracion General",
					"label": "Configuracion de Productos\Articulos",
				},
			]
		},
		
	]
	