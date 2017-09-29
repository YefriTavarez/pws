import frappe

def add_records():
	add_proyect_types()
	add_roles()

	frappe.db.commit()

def add_proyect_types():
	proyect_types = ["Muestra", "Produccion"]
	
	for proyect_type in proyect_types:
		doc = frappe.new_doc("Tipo de Proyecto")

		doc.proyect_type = proyect_type
		doc.save()

def add_roles():
	roles = [
		"Usuario de Proyectos", 
		"Supervisor de Proyectos",
		"Perfilador de Productos",
		"Ensamblador de Productos",
	]

	for role in roles:
		doc = frappe.new_doc("Role")

		doc.role_name = role
		doc.save()
