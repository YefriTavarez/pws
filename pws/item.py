import frappe

from frappe.utils import flt

from pws.api import get_parent_code

def item_autoname(doc, event):
	from frappe.model.naming import make_autoname

	item_validate(doc, event)

	if doc.item_group == "All Item Groups":
		doc.name = make_autoname("00000000.####")

		return False

	parent_codes = get_parent_code(doc.item_group, [])
	parents_code = "".join(parent_codes)

	array = [c for c in parents_code]

	missing_length = 8 - len(array)

	for e in range(missing_length):
		array.append("0")

	array += ".####"
	serie = "".join(array)

	doc.name = make_autoname(serie)

def item_validate(doc, event):
	doc.item_group = doc.item_group_4 or doc.item_group_3\
		or doc.item_group_2 or doc.item_group_1

def item_ontrash(doc, event):
	serie = doc.name[:8]
	identifier = doc.name[-4:]

	current = frappe.db.sql("""SELECT current 
		FROM tabSeries 
		WHERE name = '{}' """.format(serie), as_list=True)[0][0]

	if flt(current) == flt(identifier):
		frappe.db.sql("""
			UPDATE 
				tabSeries 
			SET 
				current = {0}
			WHERE 
				name = '{1}'
		""".format(flt(identifier) -1 if flt(identifier) > 0 else 0, serie),
		as_list=True)