# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate, cstr, cint, flt

from frappe.desk.form.assign_to import add as assign

message = "¡Estado de la Tarea no se puede cambiar mientras hayan tareas incompletas!"

class Tarea(Document):
	def onload(self):
		item = frappe.get_value("Proyecto", self.project, "item")
		fieldlist = (
			"cantidad_tiro_proceso",
			"cantidad_tiro_pantone",
			"cantidad_proceso_retiro",
			"cantidad_pantone_retiro")

		colors = frappe.get_value("Ensamblador de Productos",
			item, fieldlist) or ("", "", "", "")

		listzipped = zip(fieldlist, colors)

		self.set_onload("colors_for_sku", dict(listzipped))

	def assign_to(self):
		assign({
			"assign_to": self.user,
			"doctype": self.doctype,
			"name": self.name,
			"description": self.subject
		})

	def validate(self):
		if self.dependant and not self.status == "Open":
			for dependee in self.depends_on:

				status = frappe.get_value("Tarea", dependee.task, "status")

				if not status == "Closed" and not status == "Cancelled":
					frappe.throw(message)

		if self.get("was_closed"):
			self.after_validate()
			self.update_dependee_tasks()

		if self.enable_colors:
			self.validate_colors()

	def after_validate(self):
		project = frappe.get_doc("Proyecto", self.project)
		project.onload()

		task_number = frappe.get_value("Tarea de Proyecto", {
			"parent": project.name,
			"task_id": self.name
		}, ["idx"])

		msg = u"Cerró la tarea {0} a las {1}".format(task_number,
			frappe.utils.now_datetime())

		project.add_comment("Edit", msg, frappe.session.user, self.doctype, self.name)

		if not [task for task in project.tasks if not task.status == 'Closed']:
			project.set('status', 'Completed')
		else:
			project.set('status', 'Open')

		project.db_update()
		self.notify_project_manager_and_owner(project, msg)

	def notify_project_manager_and_owner(self, project, msg):
		from frappe import _
		__project__ = project.as_dict()
		__project__.owner_name = frappe.get_value("User", self.modified_by, "full_name")

		opts = frappe._dict({
			"delayed": False,
			"recipients": [project.project_manager, project.owner],
			"sender": frappe.get_value("Email Account", {"default_outgoing": "1"}, ["email_id"]),
			"reference_doctype": project.doctype,
			"reference_name": project.name,
			"subject": _("Finalizacion de Tarea"),
			"message": u"<b>{0}</b> cerró la tarea <i>{1}</i> del proyecto:<br><i>{2}</i>"\
				.format(__project__.owner_name, self.subject,
					__project__.title or __project__.notes)
		})

		frappe.sendmail(** opts)

	def update_dependee_tasks(self):
		from pws.api import add_to_date

		dependee_list = frappe.db.sql("""SELECT parent
			FROM `tabTarea Dependiente de`
			WHERE  task = %s""", (self.name),
		as_dict=True)

		for dependee in dependee_list:

			doc = frappe.get_doc("Tarea", dependee.parent)

			doc.exp_start_date = self.close_date

			opts = frappe._dict({
				"as_datetime": True,
				"date": self.close_date,
				doc.time_unit: doc.max_time
			})

			doc.exp_end_date = add_to_date(**opts)

			doc.db_update()

		frappe.db.commit()

	def validate_colors(self):
		if self.status != "Closed":
			return

		db_status = frappe.db.get_value("Tarea", self.name, "status")

		# if db_status == self.status:
		# 	return

		for fieldname in get_reqd_list(self):
			if self.get(fieldname):
				continue

			frappe.throw(_("Missing color for field {0}".format(fieldname)))

		# finally
		self.validate_proceso_colors()

	def validate_proceso_colors(self):
		tiro_fields = (
			"color_proceso_tiro_1",
			"color_proceso_tiro_2",
			"color_proceso_tiro_3",
			"color_proceso_tiro_4",
		)

		retiro_fields = (
			"color_proceso_retiro_1",
			"color_proceso_retiro_2",
			"color_proceso_retiro_3",
			"color_proceso_retiro_4",
		)

		tiro_original_list = [self.get(color) for color in tiro_fields\
			if self.get(color)]

		retiro_original_list = [self.get(color) for color in retiro_fields\
			if self.get(color)]

		# let's make it a set to get unique values
		tiro_set = set(tiro_original_list)
		retiro_set = set(retiro_original_list)

		# let's make it back a list with unique values
		tiro_list = list(tiro_set)
		retiro_list = list(retiro_set)

		if len(tiro_list) != len(tiro_original_list):
			frappe.throw(_("Colores duplicados en proceso tiro!"))

		if len(retiro_list) != len(retiro_original_list):
			frappe.throw(_("Colores duplicados en proceso retiro!"))

def get_reqd_list(task):
	item = frappe.get_value("Proyecto", task.project, "item")
	fieldlist = (
		"cantidad_tiro_proceso",
		"cantidad_tiro_pantone",
		"cantidad_proceso_retiro",
		"cantidad_pantone_retiro"
	)

	cantidad_tiro_proceso, cantidad_tiro_pantone, cantidad_proceso_retiro, \
		cantidad_pantone_retiro = frappe.get_value("Ensamblador de Productos",
			item, fieldlist)

	fieldlist = []

	if cint(cantidad_tiro_proceso):
		colors = cint(cantidad_tiro_proceso)

		fields = (
			"color_proceso_tiro_1",
			"color_proceso_tiro_2",
			"color_proceso_tiro_3",
			"color_proceso_tiro_4",
		)

		for idx in range(colors):
			fieldlist.append(fields[idx])

	if cint(cantidad_tiro_pantone):
		colors = cint(cantidad_tiro_pantone)

		fields = (
			"color_pantone_tiro_1",
			"color_pantone_tiro_2",
			"color_pantone_tiro_3",
			"color_pantone_tiro_4",
		)

		for idx in range(colors):
			fieldlist.append(fields[idx])

	if cint(cantidad_proceso_retiro):
		colors = cint(cantidad_proceso_retiro)

		fields = (
			"color_proceso_retiro_1",
			"color_proceso_retiro_2",
			"color_proceso_retiro_3",
			"color_proceso_retiro_4",
		)

		for idx in range(colors):
			fieldlist.append(fields[idx])

	if cint(cantidad_pantone_retiro):
		colors = cint(cantidad_pantone_retiro)

		fields = (
			"color_pantone_retiro_1",
			"color_pantone_retiro_2",
			"color_pantone_retiro_3",
			"color_pantone_retiro_4",
		)

		for idx in range(colors):
			fieldlist.append(fields[idx])

	return fieldlist
