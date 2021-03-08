# -*- coding: utf-8 -*-
# Copyright (c) 2021, Eco Data & IAC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def user_assign(doc, method):
	user = frappe.get_doc("User", doc.name)
	user.role_profile_name = "user"
	user.module_profile = "IAC"
	user.flags.ignore_permissions = 1
	user.save()
