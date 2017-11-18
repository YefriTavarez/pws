# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document

from frappe.desk.form.assign_to import add as assign

message = "¡Estado de la Tarea no se puede cambiar mientras hayan tareas incompletas!"

class Tarea(Document):
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
			"message": u"<b>{0}</b> cerró la tarea <i>{1}</i> del proyecto:<br><i>{2}</i>".format(__project__.owner_name,
				self.subject, __project__.title or __project__.notes)
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