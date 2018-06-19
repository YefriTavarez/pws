frappe.listview_settings["Solicitud de Pago"] = {
	// "hide_name_column": true,
	"add_fields": ["outstanding_amount", "status", "docstatus"],
	"get_indicator": (doc) => {
		let status = doc.status;

		if (doc.outstanding_amount == 0) {
			status = "PAGADO";
		}

		let states = {
			"PAGADO": "PAGADO|green|outstanding_amount,=,0",
			"APROBADO": "APROBADO|blue|status,=,APROBADO",
			"PENDIENTE": "PENDIENTE|orange|status,=,PENDIENTE",
			"DENEGADO": "DENEGADO|red|status,=,DENEGADO"
		};

		if (status == "APROBADO") {
			return ["APROBADO", "blue", "status,=,APROBADO|docstatus,=,1|outstanding_amount,>,0"];
		}

		return states[status].split("|");
	}
}