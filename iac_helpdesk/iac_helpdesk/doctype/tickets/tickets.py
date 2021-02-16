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
		pass
		# if self.category == "Cloud":
		# 	self.assigned_to = "ca@dev.io"

		# elif self.category == "IT":
		# 	self.assigned_to = "a@dev.io"

		# if self.assigned_to and not self.mail_sent:
		# 	mail_id = self.assigned_to

		# 	subj = 'New Ticket Notification - ' + cstr(self.name)  + ' for ' + self.category
		# 	notification_message =  'New Ticket was Generated - <a href="desk#Form/Ticket/{0}" target="_blank">{0}</a> \
		# 	for {1} Category, Against Ticket Number {2}.'.format(self.name,self.category,self.name)

		# 	frappe.sendmail(mail_id,subject=subj,\
		# 		message = notification_message)
		# 	frappe.msgprint("Ticket Raised, Email Sent Successfuly!")
		# 	self.mail_sent = '1'

		# if self.clarification and self.clarification_from and self.clarification_to and self.clarification_status == "Raised":
		# 	mail_id = self.clarification_from

		# 	subj = 'New Clarification Notification - ' + cstr(self.name)  + ' from ' + self.clarification_to
		# 	notification_message =  'New Clarification was Requested - <a href="desk#Form/Ticket/{0}" target="_blank">{0}</a> \
		# 	for {1} Category, Against Ticket Number {2}.'.format(self.name,self.category,self.name)

		# 	frappe.sendmail(mail_id,subject=subj,\
		# 		message = notification_message)


# @frappe.whitelist()
# def get_events(start, end, filters=None):
# 	"""Returns events for Course Schedule Calendar view rendering.
# 	:param start: Start date-time.
# 	:param end: End date-time.
# 	:param filters: Filters (JSON).
# 	"""
# 	from frappe.desk.calendar import get_event_conditions
# 	conditions = get_event_conditions("Tickets", filters)

# 	data = frappe.db.sql("""select name, status, category,
# 			timestamp(date, time) as from_datetime,
# 			timestamp(date, time) as to_datetime,
# 			0 as 'allDay'
# 		from `tabTickets`
# 		where ( date between %(start)s and %(end)s )
# 		{conditions}""".format(conditions=conditions), {
# 			"start": start,
# 			"end": end
# 			}, as_dict=True, update={"allDay": 0})

# 	return data


@frappe.whitelist()
def get_permissions(user):
	retval = ''
	if "System Manager" in frappe.permissions.get_roles(frappe.session.user):
		pass
	
	elif "Admin" in frappe.permissions.get_roles(frappe.session.user):
		cat_list = frappe.db.sql("""select name from tabTickets Category""",as_dict = True)
		for i in cat_list:
			retval = """((`tabTickets`.category = '{i}' ) or (`tabTickets`.owner = '{user}' or 
				`tabTickets`.modified_by = '{user}'))""".format(i = 'IT', user=frappe.session.user)
	
	elif "Cloud Admin" in frappe.permissions.get_roles(frappe.session.user):
		cat_list = frappe.db.sql("""select name from tabTickets Category""",as_dict = True)
		for i in cat_list:
			retval = """((`tabTickets`.category = '{i}' ) or (`tabTickets`.owner = '{user}' or 
				`tabTickets`.modified_by = '{user}'))""".format(i = 'Cloud', user=frappe.session.user)

	elif "Users" in frappe.permissions.get_roles(frappe.session.user):
		retval = """((`tabTickets`.owner = '{user}' or 
				`tabTickets`.modified_by = '{user}'))""".format(user=frappe.session.user)


	return retval


