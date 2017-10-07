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
	"Custom Script", 
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
# doctype_js = {"doctype" : "public/js/doctype.js"}
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
		"autoname": "pws.api.item_autoname",
		"validate": "pws.api.item_validate",
		"on_trash": "pws.api.item_ontrash",
	},
	"Item Group": {
		"autoname": "pws.api.item_group_autoname",
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
