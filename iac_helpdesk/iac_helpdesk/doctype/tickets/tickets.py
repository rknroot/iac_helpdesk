# -*- coding: utf-8 -*-
# Copyright (c) 2021, Eco Data & IAC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr, getdate

class Tickets(Document):
	def validate(self):
		if self.category == "Cloud":
			self.assigned_to = "ca@dev.io"

		elif self.category == "IT":
			self.assigned_to = "a@dev.io"

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Course Schedule Calendar view rendering.
	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Tickets", filters)

	data = frappe.db.sql("""select name, status, category,
			timestamp(date, time) as from_datetime,
			timestamp(date, time) as to_datetime,
			0 as 'allDay'
		from `tabTickets`
		where ( date between %(start)s and %(end)s )
		{conditions}""".format(conditions=conditions), {
			"start": start,
			"end": end
			}, as_dict=True, update={"allDay": 0})

	return data

# @frappe.whitelist()
# def get_permissions(user):
# 	# role = frappe.get_roles(assigned_to)
# 	frappe.errprint(role)
# 	retval = ''
# 	if "System Manager" in frappe.permissions.get_roles(frappe.session.user):
# 		pass
# 	elif "Admin" in frappe.permissions.get_roles(frappe.session.user):
# 		frappe.msgprint(frappe.get_roles(frappe.session.user))
# 		cat_list = frappe.db.sql("""select name from tabTickets Category""",as_dict = True)
# 		frappe.msgprint('cat '+str(cat_list))
# 		for i in cat_list:
# 			retval = """((`tabTickets`.category = '{i}' ) )""".format(i = 'IT')

# 	return retval


