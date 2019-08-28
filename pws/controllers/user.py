import frappe

def get_first_name(user):
	# assign to a local variable
	# to comply with DRY

	first_name = user.first_name or ""

	parts = first_name.split()

	return parts[0] if parts else ""


def get_last_name(user):
	# assign to a local variable
	# to comply with DRY

	last_name = user.last_name or ""

	parts = last_name.split()

	return parts[0] if parts else ""


def get_username(user):
	first_name = get_first_name(user)
	last_name = get_last_name(user)

	return "_".join((first_name, last_name))
