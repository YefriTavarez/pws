// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Solicitud de Diligencia', {
	"setup": function(frm) {
		frm.set_query("party_type", function() {
			return {
				"query": "pws.queries.doctype_query"
			};
		});

		frm.set_query("project", function() {
			return {
				"filters": {
					"customer": frm.doc.party_type == "Customer"? frm.doc.party: ["LIKE", "%"]
				}
			};
		});

		frm.set_query("party_address", function() {
			return {
				"query": "frappe.contacts.doctype.address.address.address_query",
				"filters": {
					"link_doctype": frm.doc.party_type || ["LIKE", "%"],
					"link_name": frm.doc.party || ["LIKE", "%"],
				}
			}
		});

		frm.toggle_reqd("notes", frm.doc.status == "DENEGADO");
	},
	"onload": function(frm) {
		frm.add_fetch("project", "title", "project_name");
	},
	"party_type": function(frm) {
		frm.set_value("party", undefined);
	},
	"party": function(frm) {
		frm.trigger("party_address");
	},
	"status": function(frm) {
		frm.toggle_reqd(["notes", "denied_by"], frm.doc.status == "DENEGADO");
		frm.toggle_reqd(["approved_by"], frm.doc.status == "APROBADO");
	},
	"motivation": function(frm) {
		frm.set_value_if_missing("description", frm.doc.motivation);
	},
	"other_destination": function(frm) {
		frm.toggle_reqd("destination", frm.doc.other_destination);

		if (frm.doc.other_destination) {
			var field_list = ["party_address", "display_address"];

			$.map(field_list, function(field) {
				frm.doc[field] = undefined;
			});
			
			refresh_field(field_list);
		}
	},
	"party_address": function(frm) {
		frm.call("update_address", "args", function(response) {
			frm.refresh();
		});
	},
});
