# -*- coding: utf-8 -*-
# Copyright (c) 2021, Eco Data & IAC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate
from erpnext.education.utils import OverlapError

class RecurrenceTicketCreationTool(Document):

	def schedule_ticket(self):
		"""Creates tickets as per specified parameters"""

		tickets_schedule = []
		tickets_schedule_errors = []

		self.validate_mandatory()
		self.validate_date()

		date = self.from_date
		while date < self.to_date:
			if self.day == calendar.day_name[getdate(date).weekday()]:
				ticket_schedule = self.make_tickets_schedule(date)
				try:
					print('pass')
					ticket_schedule.save()
				except OverlapError:
					print('fail')
					tickets_schedule_errors.append(date)
				else:
					tickets_schedule.append(ticket_schedule)

				date = add_days(date, 7)
			else:
				date = add_days(date, 1)

		return dict(
			tickets_schedule=tickets_schedule,
			tickets_schedule_errors=tickets_schedule_errors,
		)

	def validate_mandatory(self):
		"""Validates all mandatory fields"""

		fields = ['category', 'description', 'from_date', 'to_date', 'day']
		for d in fields:
			if not self.get(d):
				frappe.throw(_("{0} is mandatory").format(
					self.meta.get_label(d)))

	def validate_date(self):
		"""Validates if Course Start Date is greater than Course End Date"""
		if self.from_date > self.to_date:
			frappe.throw(
				"Tickets From Date cannot be greater than To Date.")

	def make_tickets_schedule(self, date):
		"""Makes a new Course Schedule.
		:param date: Date on which Course Schedule will be created."""

		ticket_schedule = frappe.new_doc("Tickets")
		ticket_schedule.category = self.category
		ticket_schedule.description = self.description
		ticket_schedule.date = date
		return ticket_schedule

