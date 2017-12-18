# -*- coding: utf-8 -*-
# Copyright (c) 2017, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint, nowdate

from erpnext.accounts.party import get_party_account
from erpnext.accounts.utils import get_account_currency, get_balance_on

class SolicituddePago(Document):
	def after_insert(self):
		self.validate_past_required_by()
		self.notify_payment_request_approvers()

	def validate(self):
		self.validate_mandatory_party()
		self.validate_approved_amount()
		self.validate_references()
		self.validate_notes()
		self.update_approved_amount()

	def on_submit(self):
		self.validate_change_status()
		self.validate_disbursement_account()
		self.validate_signatures()
		self.notify_payment_request_user()

	def validate_mandatory_party(self):
		if not self.party and not self.other_party:
			frappe.throw("""¡No se especifico ningún tercero para esta solicitud!""")

	def validate_approved_amount(self):
		if self.approved_amount > self.requested_amount:
			frappe.throw("""¡Monto aprobado no puede ser mayor que el monto solicitado!""")

	def validate_past_required_by(self):
		now_datetime = frappe.utils.now_datetime()
		time_diff = frappe.utils.time_diff_in_seconds(self.required_before, now_datetime)

		if time_diff < 0:
			frappe.throw("""¡La fecha requerida no puede ser menor que la fecha actual!""")

	def validate_change_status(self):
		if self.status == "PENDIENTE":
			frappe.throw("""¡Para validar el estado debe ser diferente de PENDIENTE!""")

	def validate_disbursement_account(self):
		if not self.disbursement_account:
			frappe.throw("""¡Seleccione la cuenta de desembolso antes de validar!""")

	def validate_signatures(self):
		conf = frappe.get_single("Configuracion General")

		signatures_list = []
		for signature in ["approved_by", "reviewed_by", "ceo"]:
			if self.get(signature):
				signatures_list.append(signature)

		missing_signatures = cint(conf.signatures_for_payment_request) - len(signatures_list)
		if missing_signatures > 0:
			frappe.throw("""¡{0} {2} {1} para poder validar!"""
				.format("Faltan" if missing_signatures > 1 else "Falta",
					"firmas" if missing_signatures > 1 else "firma", missing_signatures))

	def validate_notes(self):
		if self.status == "DENEGADO" and not self.notes:
			frappe.throw("""¡Solicitud de pago fue DENEGADA y no posee una justificación!""")

	def validate_references(self):
		if self.reference_name and not self.reference_date:
			frappe.throw("""¡Fecha de referencia requerida si esta el Numero de Referencia!""")

		if not self.reference_name and self.reference_date:
			frappe.throw("""¡Numero de referencia requerido si esta la Fecha de Referencia!""")
	def validate_party_type_for_payment_entry(self):
		if self.party_type == "Other":
			frappe.throw("¡No puede hacer un pago a una Entidad desconocida!")

	def update_approved_amount(self):
		if self.owner == frappe.session.user:
			self.approved_amount = self.requested_amount
			self.outstanding_amount = self.requested_amount
		else:
			self.outstanding_amount = self.approved_amount

	def notify_payment_request_user(self):
		notify_payment_request_user(self)

	def notify_payment_request_approvers(self):
		notify_payment_request_approvers(self)

	def make_payment_entry(self):
		return make_payment_entry(self.doctype, self.name)

def notify_payment_request_approvers(self):
	doc = self.as_dict()
	doc.owner_name = frappe.get_value("User", self.owner, "full_name")
	doc.hostname = frappe.conf.get("hostname")
	conf = frappe.get_single("Configuracion General")

	opts = frappe._dict({
		"delayed": False,
		"recipients": [approver.user for approver in conf.payment_request_approvers],
		"sender": frappe.get_value("Email Account", {"default_outgoing": "1"}, ["email_id"]),
		"reference_doctype": doc.doctype,
		"reference_name": doc.name,
		"subject": "Nueva Solicitud de Pago | {}".format(doc.motivation),
		"message": """<i>%(owner_name)s</i> ha creado la Solicitud de Pago No: 
			<strong>
				<a href="%(hostname)s/Form/%(doctype)s/%(name)s">%(name)s</a>
			</strong>

			<br>
			<p>%(motivation)s</p>
		""" % doc
	})

	frappe.sendmail(** opts)

def notify_payment_request_user(self):
	doc = self.as_dict()
	doc.approver = frappe.get_value("User", self.modified_by, "full_name")
	doc.hostname = frappe.conf.get("hostname")
	conf = frappe.get_single("Configuracion General")

	opts = frappe._dict({
		"delayed": False,
		"recipients": [self.owner],
		"sender": frappe.get_value("Email Account", {"default_outgoing": "1"}, ["email_id"]),
		"reference_doctype": doc.doctype,
		"reference_name": doc.name,
		"subject": "Nueva Solicitud de Pago | {}".format(doc.motivation),
		"message": """<i>%(approver)s</i> ha %(status)s su Solicitud de Pago No: 
			<strong>
				<a href="%(hostname)s/Form/%(doctype)s/%(name)s">%(name)s</a>
			</strong>

			<br>
			<p>%(motivation)s</p>
			<p>%(notes)s</p>
		""" % doc
	})

	frappe.sendmail(** opts)

@frappe.whitelist()
def make_payment_entry(dt, dn):
	doc = frappe.get_doc(dt, dn)

	doc.validate_party_type_for_payment_entry()

	payment_entry = frappe.new_doc("Payment Entry")
	default_company = frappe.defaults.get_global_default("company")
	company_currency = frappe.get_value("Company", default_company, "default_currency")

	party_account = get_party_account(doc.party_type, doc.party or doc.other_party, default_company)
	party_name = frappe.get_value(doc.party_type, doc.party, "{}_name".format(doc.party_type.lower()))

	payment_entry.payment_type = "Pay"
	payment_entry.company = default_company
	payment_entry.posting_date = nowdate()
	payment_entry.mode_of_payment = doc.get("mode_of_payment")
	payment_entry.party_type = doc.party_type
	payment_entry.party_balance = get_balance_on(party_account, nowdate(), doc.party_type, doc.party, default_company)
	payment_entry.party = doc.party or doc.other_party
	payment_entry.party_name =  party_name or doc.other_party
	payment_entry.paid_from = doc.disbursement_account
	payment_entry.paid_to = party_account
	payment_entry.paid_from_account_currency = get_account_currency(doc.disbursement_account) or doc.currency
	payment_entry.paid_to_account_currency = get_account_currency(party_account) or doc.currency
	payment_entry.paid_from_account_balance = get_balance_on(doc.disbursement_account, nowdate())
	payment_entry.paid_to_account_balance = get_balance_on(party_account, nowdate(), company=default_company)
	payment_entry.paid_amount = doc.approved_amount
	payment_entry.received_amount = doc.approved_amount
	payment_entry.allocate_payment_amount = 1
	payment_entry.payment_request = doc.name
	# payment_entry.letter_head = doc.get("letter_head")

	payment_entry.append("references", {
		"reference_doctype": dt,
		"reference_name": dn,
		"bill_no": doc.get("reference_name"),
		"due_date": doc.get("reference_date"),
		"total_amount": doc.approved_amount,
		"outstanding_amount": 0.000,
		"allocated_amount": doc.approved_amount
	})

	payment_entry.setup_party_account_field()
	# payment_entry.set_missing_values()

	payment_entry.set_exchange_rate()
	payment_entry.set_amounts()
	return payment_entry.as_dict()

