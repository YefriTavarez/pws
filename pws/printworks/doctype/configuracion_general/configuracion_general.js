// Copyright (c) 2017, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Configuracion General', {
	"refresh": (frm) => {
		$.map(["set_queries"], (event) => frm.trigger(event));
	},
	"set_queries": (frm) => {
		$.map(["set_item_group_query", "materials_item_group_query", "set_chores_approver_query"], 
			(query) => frm.trigger(query));
	},
	"set_item_group_query": (frm) => {
		frm.set_query("item_group", () => {
			return {
				"filters": { "is_group": 1 }
			};
		});
	},
	"materials_item_group_query": (frm) => {
		frm.set_query("materials_item_group", () => {
			return {
				"filters": { "parent_item_group": "All Item Groups" }
			};
		});	
	},
	"set_chores_approver_query": (frm) => {
		frm.set_query("chores_approver", () => {
			return {
				"query": "pws.queries.user_query",
				"filters": { "role": "Logistica" }
			};
		});	
	}
});
