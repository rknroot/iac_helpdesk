# -*- coding: utf-8 -*-
# Copyright (c) 2021, Eco Data & IAC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr, getdate
import calendar
from frappe import _
from six.moves import range
from six import string_types
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe.utils.user import get_enabled_system_users
from frappe.desk.reportview import get_filters_cond
from datetime import date, time, datetime, timedelta
from frappe.model.naming import make_autoname, parse_naming_series


weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

class Tickets(Document):
	def onload(self):
		if self.create_recurrence_ticket:
			parent_ticket = frappe.db.get_all("Tickets",filters={"parent_ticket":self.name},fields=('name','ticket_date','status'))
			for i in parent_ticket:
				child = self.append('child_tickets',{})
				#frappe.db.set_value('')
				child.title = i.name
				child.status = i.status
				child.ticket_date = i.ticket_date

	def validate(self):
		if self.category == "Cloud":
			self.assigned_to = "ca@dev.io"

		elif self.category == "IT":
			self.assigned_to = "a@dev.io"

	def autoname(self):
		ticket_series = frappe.db.get_single_value("Tickets Settings","ticket_series")
		if not self.parent_ticket:
			self.name = make_autoname(ticket_series)
		if self.parent_ticket:
			self.name = make_autoname(self.parent_ticket + '.-.##')


@frappe.whitelist()
def get_tickets(start, end, user=None, for_reminder=False, filters=None):
	if isinstance(filters, string_types):
		filters = json.loads(filters)

	filter_condition = get_filters_cond('Tickets', filters, [])
	#frappe.msgprint(str(user))
	tables = ["`tabTickets`"]

	events = frappe.db.sql("""
		SELECT `tabTickets`.name,
				`tabTickets`.ticket_date,
				`tabTickets`.priority,
				`tabTickets`.category,
				`tabTickets`.description,
				`tabTickets`.owner,
				`tabTickets`.create_recurrence_ticket,
				`tabTickets`.repeat_on,
				`tabTickets`.repeat_till,
				`tabTickets`.monday,
				`tabTickets`.tuesday,
				`tabTickets`.wednesday,
				`tabTickets`.thursday,
				`tabTickets`.friday,
				`tabTickets`.saturday,
				`tabTickets`.sunday,
				`tabTickets`.parent_ticket
		FROM {tables}
		WHERE (
				(
					(date(`tabTickets`.ticket_date) BETWEEN date(%(start)s) AND date(%(end)s))
					OR (date(`tabTickets`.ticket_date) BETWEEN date(%(start)s) AND date(%(end)s))
					OR (
						date(`tabTickets`.ticket_date) <= date(%(start)s)
						AND date(`tabTickets`.ticket_date) >= date(%(end)s)
					)
				)
				AND (
					date(`tabTickets`.ticket_date) <= date(%(start)s)
					AND `tabTickets`.create_recurrence_ticket=1
					AND coalesce(`tabTickets`.repeat_till, '3000-01-01') > date(%(start)s)
					AND `tabTickets`.name = (%(user)s)
				)
			)
		{filter_condition}
		ORDER BY `tabTickets`.ticket_date""".format(
			tables=", ".join(tables),
			filter_condition=filter_condition
		), {
			"start": start,
			"end": end,
			"user": user,
		}, as_dict=1)


	# process recurring events
	start = start.split(" ")[0]
	end = end.split(" ")[0]
	add_events = []
	remove_events = []

	def add_event(e, date):
		new_event = e.copy()
		#frappe.msgprint('new' + str(new_event))
		enddate = add_days(date,int(date_diff(e.ticket_date.split(" ")[0], e.ticket_date.split(" ")[0]))) \
			if (e.ticket_date and e.ticket_date) else date
		#frappe.msgprint('enddate'+str(enddate))
		new_event.ticket_date = date + " " + e.ticket_date.split(" ")[1]
		#frappe.msgprint('start'+str(new_event.starts_on))
		new_event.ticket_date = new_event.ticket_date = enddate + " " + e.ticket_date.split(" ")[1] if e.ticket_date else None
		#frappe.msgprint('end'+str(new_event.ends_on))
		
		add_events.append(new_event)
		#frappe.msgprint('add event'+str(add_events))

	for e in events:
		if e.create_recurrence_ticket:
			e.ticket_date = get_datetime_str(e.ticket_date)
			e.ticket_date = get_datetime_str(e.ticket_date) if e.ticket_date else None

			event_start, time_str = get_datetime_str(e.ticket_date).split(" ")

			repeat = "3000-01-01" if cstr(e.repeat_till) == "" else e.repeat_till

			if e.repeat_on == "Yearly":
				start_year = cint(start.split("-")[0])
				end_year = cint(end.split("-")[0])

				# creates a string with date (27) and month (07) eg: 07-27
				event_start = "-".join(event_start.split("-")[1:])

				# repeat for all years in period
				for year in range(start_year, end_year+1):
					date = str(year) + "-" + event_start
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) and getdate(date) <= getdate(repeat):
						add_event(e, date)

				remove_events.append(e)

			if e.repeat_on == "Monthly":
				# creates a string with date (27) and month (07) and year (2019) eg: 2019-07-27
				date = start.split("-")[0] + "-" + start.split("-")[1] + "-" + event_start.split("-")[2]

				# last day of month issue, start from prev month!
				try:
					getdate(date)
				except ValueError:
					date = date.split("-")
					date = date[0] + "-" + str(cint(date[1]) - 1) + "-" + date[2]

				start_from = date
				for i in range(int(date_diff(end, start) / 30) + 3):
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) \
						and getdate(date) <= getdate(repeat) and getdate(date) >= getdate(event_start):
						add_event(e, date)

					date = add_months(start_from, i+1)
					#frappe.msgprint(str(date))
				remove_events.append(e)

			if e.repeat_on == "Weekly":
				for cnt in range(date_diff(end, start) + 1):
					date = add_days(start, cnt)
					if getdate(date) >= getdate(start) and getdate(date) <= getdate(end) \
						and getdate(date) <= getdate(repeat) and getdate(date) >= getdate(event_start) \
						and e[weekdays[getdate(date).weekday()]]:
						add_event(e, date)
					#frappe.msgprint(str(date))

				remove_events.append(e)

			if e.repeat_on == "Daily":
				#frappe.msgprint('inside daily '+str(date_diff(end,start)))
				#frappe.msgprint('end '+str(end) + ' start '+str(start))
				#start_increment = start + timedelta(days="1")
				for cnt in range(date_diff(end, start) + 1):
					#frappe.msgprint('count'+str(cnt))
					date = add_days(start, cnt)
					if getdate(date) >= getdate(event_start) and getdate(date) <= getdate(end) and getdate(date) <= getdate(repeat):
						#frappe.msgprint('final date '+str(date))
						add_event(e, date)
				
				remove_events.append(e)

	for e in remove_events:
		events.remove(e)

	events = events + add_events
	#frappe.msgprint(str(events))
	for e in events:
		ticket_schedule = frappe.new_doc("Tickets")
		ticket_schedule.category = e.category
		ticket_schedule.priority = e.priority
		ticket_schedule.description = e.description
		ticket_schedule.ticket_date = e.ticket_date
		ticket_schedule.parent_ticket = e.name
		ticket_schedule.flags.ignore_permissions = 1
		ticket_schedule.insert()
		
		
		#return ticket_schedule
		# remove weekday properties (to reduce message size)
		#for w in weekdays:
			#del e[w]
	
	#return events
@frappe.whitelist()
def del_duplicate(start):
	# frappe.msgprint('call'+str(start))
	get_tickets_duplicate = frappe.db.sql("""select name, ticket_date, create_recurrence_ticket from `tabTickets` where ticket_date = %s""",(start),as_dict=1)
	for i in get_tickets_duplicate:
		#frappe.msgprint(str(i.create_recurrence_ticket))
		if i.create_recurrence_ticket == 0:
			#frappe.msgprint('DEL'+str(i.name))
			frappe.db.sql("""delete from `tabTickets` where name = %s""",(i.name))

# @frappe.whitelist()
# def update_child(start):
# 	self = frappe.get_doc('Tickets', start)
# 	if self.create_recurrence_ticket:
# 		parent_ticket = frappe.db.get_all("Tickets",filters={"parent_ticket":self.name},fields=('name','ticket_date','status'))
# 		for i in parent_ticket:
# 			child = self.append('child_tickets',{})
# 			child.title = i.name
# 			child.status = i.status
# 			child.ticket_date = i.ticket_date
# 			frappe.msgprint('call save')
# 			self.save()


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
			timestamp(ticket_date, time) as from_datetime,
			timestamp(ticket_date, time) as to_datetime,
			0 as 'allDay'
		from `tabTickets`
		where ( ticket_date between %(start)s and %(end)s )
		{conditions}""".format(conditions=conditions), {
			"start": start,
			"end": end
			}, as_dict=True, update={"allDay": 0})

	return data


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



