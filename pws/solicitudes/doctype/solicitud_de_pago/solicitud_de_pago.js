// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Solicitud de Pago', {
	"refresh": (frm) => {
		frappe.run_serially([
			frm.trigger("set_queries"),
			frm.trigger("set_reqd_fields"),
			frm.trigger("show_hide_fields"),
			frm.trigger("enable_disable_refernce_fields"),
			frm.trigger("add_custom_buttons"),
		]);
	},
	"onload": (frm) => {
		frappe.run_serially([
			frm.trigger("set_user_info"),
			frm.trigger("save_doc_status"),
		]);
	},
	"set_user_info": (frm) => {
		let user_fullname = frappe.session.user_fullname;
		let user_department = frappe.boot.user.department;

		if (frm.is_new()) {
			frm.set_value_if_missing("full_name", user_fullname);
			frm.set_value_if_missing("department", user_department || "General");
		}
	},
	"validate": (frm) => {
		// frm.trigger("validate_required_before");
	},
	"party_type": (frm) => {
		frappe.run_serially([
			frm.set_value("party", undefined),
			frm.set_value("other_party", undefined),
			frm.toggle_reqd("party", frm.doc.party_type != "Other"),
			frm.toggle_reqd("other_party", frm.doc.party_type == "Other"),
		]);
	},
	"make_payment_entry": (frm) => {
		let opts = {
			"method": "pws.api.make_payment_entry"
		};

		opts.args = {
			"doctype": frm.doctype,
			"name": frm.docname
		};

		frappe.call(opts).then((response) => {
			doc = frappe.model.sync(response.message)[0];
			frappe.set_route("Form", doc.doctype, doc.name);
		}, (error) => frappe.msgprint("¡Hubo un problema mientras se hacia el pago!"))
	},	
	"make_journal_entry": (frm) => {
		let opts = {
			"method": "pws.api.make_journal_entry"
		};

		opts.args = {
			"doctype": frm.doctype,
			"name": frm.docname
		};

		frappe.call(opts).then((response) => {
			doc = frappe.model.sync(response.message)[0];
			frappe.set_route("Form", doc.doctype, doc.name);
		}, (error) => frappe.msgprint("¡Hubo un problema mientras se hacia el pago!"))
	},
	"status": (frm) => {
		frappe.run_serially([
			frm.trigger("validate_status_change"),
			frm.toggle_reqd("notes", frm.doc.status == "DENEGADO"),
			frm.trigger("set_reqd_fields"),
			frm.refresh()
		]);
	},
	"requested_amount": (frm) => {
		frm.set_value("approved_amount", frm.doc.requested_amount);
	},
	"required_before": (frm) => frm.trigger("validate_required_before"),
	"save_doc_status": (frm) => frm.doc.initial_status = frm.doc.status,
	"add_custom_buttons": (frm) => {
		if (frm.doc.docstatus == 1 && frm.doc.status == "APROBADO") {
			if (frm.doc.outstanding_amount && frm.doc.party_type != "Other") {
				frm.add_custom_button("Pago", () => frm.trigger("make_payment_entry"), "Hacer");
			}
			
			frm.add_custom_button("Asiento", () => frm.trigger("make_journal_entry"), "Hacer");
			frm.page.set_inner_btn_group_as_primary("Hacer");
		}
	},
	"set_queries": (frm) => {
		$.map([
			"set_party_query", "set_bank_account_query"
		], (query) => frm.trigger(query));
	},
	"set_party_query": (frm) => {
		frm.set_query("party_type", () => {
			return {
				"filters": {
					"name": ["in", 
						["Supplier", "Employee", "Other"]
					]
				}
			};
		});
	},
	"set_bank_account_query": (frm) => {
		frm.set_query("disbursement_account", () => {
			if (["Bank", "Cash"].includes(frm.doc.type)) {
				return {
					"filters": {
						"account_type": frm.doc.type,
						"account_currency": frm.doc.currency
					}
				};
			}
		});
	},
	"validate_required_before": (frm) => {
		let now_datetime = frappe.datetime.now_datetime();

		if (frm.doc.required_before <= now_datetime) {
			frappe.throw("¡La fecha requerida no puede ser menor que la fecha actual!");
		}
	},
	"validate_status_change": (frm) => {
		if (frm.doc.initial_status != "PENDIENTE") {
			if (frm.doc.status == "PENDIENTE") {
				setTimeout(() => frm.set_value("status", frm.doc.initial_status), 100);
				frappe.throw(__("¡No puede cambiar estado de {0} a {1}!", 
					[frm.doc.initial_status, frm.doc.status]));
			}
		}
	},
	"enable_disable_refernce_fields": (frm) => {
		if (0.000 < cint(frm.doc.docstatus)) {
			$.map(["reference_name", "reference_date"], (field) => 
				frm.toggle_enable(field, ! frm.doc.reference_name));
		}
	},
	"show_hide_fields": (frm) => {
		let is_ceo = frappe.user.has_role(["CEO"]);
		let is_accounts_manager = frappe.user.has_role(["Contador"]);
		let is_finance_manager = frappe.user.has_role(["Gerente Financiero", "Gerente Administrativo"]);

		if (is_ceo) {
			$.map(["ceo", "status"], (field) => frm.toggle_enable(field, true));
		} else if (is_finance_manager) {
			$.map(["approved_by", "approved_amount", "status"], (field) => frm.toggle_enable(field, true));
		} else if (is_accounts_manager) {
			$.map(["reviewed_by", "status"], (field) => frm.toggle_enable(field, true));
		} else {
			$.map(["mode_of_payment",
				"disbursement_account",
				"reference_name",
				"reference_date", 
				"notes"], 
			(field) => frm.toggle_enable(field, false));
		}

		if (frm.doc.owner == frappe.session.user || frm.is_new()) {
			$.map(["requested_by"], (field) => frm.toggle_enable(field, true));
		} else {
			$.map(["party_type",
				"party",
				"other_party",
				"posting_date",
				"required_before",
				"requested_amount",
				"motivation"], 
			(field) => frm.toggle_enable(field, false));
		}
	},
	"set_reqd_fields": (frm) => {
		frm.toggle_reqd("mode_of_payment", frm.doc.status == "APROBADO");
	}
});
