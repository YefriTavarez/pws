frappe.listview_settings["Solicitud de Diligencia"] = {
	"hide_name_column": true,
	"add_fields": ["status", "docstatus"],
	"get_indicator": function(doc) {
		if (doc.status == "PENDIENTE") {
			return ["Pendiente", "orange", "status,=,PENDIENTE"];
		}

		if (doc.status == "APROBADO") {
			return ["Aprobado", "green", "status,=,APROBADO"];
		}

		if (doc.status == "DENEGADO") {
			return ["Denegado", "red", "status,=,DENEGADO"];
		}
	}
}
