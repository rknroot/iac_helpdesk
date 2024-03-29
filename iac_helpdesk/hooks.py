# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "iac_helpdesk"
app_title = "IAC Helpdesk"
app_publisher = "Eco Data & IAC"
app_description = "IAC Digital Infrastructure Support Portal"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "rk@ecodata.in"
app_license = "MIT"

# Includes in <head>
# ------------------
calendars = ["Tickets"]
# include js, css files in header of desk.html
# app_include_css = "/assets/iac_helpdesk/css/iac_helpdesk.css"
# app_include_js = "/assets/iac_helpdesk/js/iac_helpdesk.js"

# include js, css files in header of web template
# web_include_css = "/assets/iac_helpdesk/css/iac_helpdesk.css"
# web_include_js = "/assets/iac_helpdesk/js/iac_helpdesk.js"

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
# get_website_user_home_page = "iac_helpdesk.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "iac_helpdesk.install.before_install"
# after_install = "iac_helpdesk.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "iac_helpdesk.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Tickets": "iac_helpdesk.iac_helpdesk.doctype.tickets.tickets.get_permissions"
 #	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
}
#
# has_permission = {
# 	"Tickets": "iac_helpdesk.iac_helpdesk.doctype.tickets.tickets.has_permission"
# # 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
#Hook on document methods and events

doc_events = {
	"User": {
		"after_insert": "iac_helpdesk.iac_helpdesk.doctype.api.user_assign"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"iac_helpdesk.tasks.all"
# 	],
# 	"daily": [
# 		"iac_helpdesk.tasks.daily"
# 	],
# 	"hourly": [
# 		"iac_helpdesk.tasks.hourly"
# 	],
# 	"weekly": [
# 		"iac_helpdesk.tasks.weekly"
# 	]
# 	"monthly": [
# 		"iac_helpdesk.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "iac_helpdesk.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "iac_helpdesk.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "iac_helpdesk.task.get_dashboard_data"
# }
fixtures = ["Workspace", "System Settings", "Role", "Module Profile", "Role Profile", "Workflow", "Workflow State", "Workflow Action Master"]

