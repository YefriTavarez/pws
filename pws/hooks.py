# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "pws"
app_title = "PRINTWORKS"
app_publisher = "Yefri Tavarez"
app_description = "An application for customizing some ERPNext features."
app_icon = "octicon octicon-dashboard"
app_color = "#346"
app_email = "yefritavarez@gmail.com"
app_license = "General Public License, v3"

# fixtures
fixtures = [
	"Custom Field"
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/pws/css/pws.css"
app_include_js = "/assets/pws/js/pws.js"

# include js, css files in header of web template
# web_include_css = "/assets/pws/css/pws.css"
# web_include_js = "/assets/pws/js/pws.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Order" : "public/js/purchase_order.js",
	"Payment Entry" : "public/js/payment_entry.js",
	"Translation" : "public/js/translation.js"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "pws.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pws.install.before_install"
after_install = "pws.install.add_records"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "pws.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item": {
		"autoname": "pws.item.item_autoname",
		"validate": "pws.item.item_validate",
		"on_trash": "pws.item.item_ontrash",
	},
	"Item Group": {
		"autoname": "pws.api.item_group_autoname",
	},
	"Purchase Invoice": {
		"validate": "pws.pinv.validate",
	},
	"Purchase Order": {
		"on_submit": "pws.po.on_submit"
	},
	"Sales Invoice": {
		"autoname": "pws.sinv.sinv_autoname",
	},
	"Sales Order": {
		"validate": "pws.sales_order.validate",
	},
	"File": {
		"after_insert": "pws.file.after_insert"
	},
	"Payment Entry": {
		"on_submit": "pws.payment_entry.on_submit",
		"on_cancel": "pws.payment_entry.on_cancel",
	},
	"Workstation": {
		"autoname": "pws.workstation.autoname",
	},
	"Employee": {
		"autoname": "pws.employee.autoname",
	},
	"Journal Entry": {
		"on_submit": "pws.journal_entry.on_submit",
		"on_cancel": "pws.journal_entry.on_cancel",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"pws.tasks.all"
	],
	"daily": [
		"pws.tasks.daily"
	],
	"hourly": [
		"pws.tasks.hourly"
	],
	"weekly": [
		"pws.tasks.weekly"
	],
	"monthly": [
		"pws.tasks.monthly"
	]
}

# Testing
# -------

# before_tests = "pws.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pws.event.get_events"
# }

on_session_creation = ["pws.api.on_session_creation"]

website_context = {
	"logo": "/assets/pws/images/favicon.png",
	"splash_image": "/assets/pws/images/erp-icon.svg"
}

default_mail_footer = """
"""

boot_session = [
	"pws.boot.add_user_info",
	"pws.boot.get_task_list",
]