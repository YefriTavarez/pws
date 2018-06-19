frappe.ui.form.on("Translation", {
	"refresh": (frm) => {
		if ( ! frm.is_new()){
			frm.add_custom_button(__("Duplicate"), function(event){
				$.map(["source_name", "target_name"], (fieldname) => frm.set_value(fieldname, ""));
				frm.copy_doc();
			});
		}
	}
});