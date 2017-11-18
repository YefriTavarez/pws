import frappe

from frappe import _

def get_data():
	return {
		# "no_standard_fields": "proyecto",
		# # "internal_links": "proyecto",
		# "transactions": [
		# 	{
		# 		"label": _("Proyecto"),
		# 		"items": ["Tarea"] 
		# 	}
		# ]
	}
	# return {
	# 	'fieldname': 'project',
	# 	'transactions': [
	# 		{
	# 			'label': _('Sales'),
	# 			'items': ['Sales Order', 'Sales Invoice']
	# 		},
	# 		{
	# 			'label': _('Buying'),
	# 			'items': ['Purchase Order', 'Purchase Receipt', 'Purchase Invoice']
	# 		}
	# 	]
	# }