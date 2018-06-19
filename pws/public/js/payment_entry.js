frappe.ui.form.on("Payment Entry", {
	"setup": (frm) => {
		frm.set_query("payment_request", "solicitudes_de_pago", () => {
			return {
				"filters": {
					"party": frm.doc.party,
					"outstanding_amount": [">", 0.000]
				}
			};
		});
	}
});