frappe.ui.form.on("Purchase Order", {
	"onload_post_render": (frm) => {
		if (frm.doc.docstatus != 1) {
			return 0;
		}

		if (["To Receive and Bill", "To Bill"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Payment Request"), () =>
				frm.trigger("make_payment_request"), __("Make"));
		}
	},
	"make_payment_request": (frm) => {
		let opts = {
		    "method": "pws.po.make_payment_request"
		};
		
		opts.args = {
			"doctype": frm.doctype,
			"docname": frm.docname,
		};
		
		frappe.call(opts).done((response) => {
			let payment_request = response.message;
		
			if (payment_request) {
				let doc = frappe.model.sync(payment_request)[0];
				frappe.render_doc(doc);
			}
		});
	}
});