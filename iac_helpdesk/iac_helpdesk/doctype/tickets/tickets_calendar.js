frappe.views.calendar["Tickets"] = {
	field_map: {
		// from_datetime and to_datetime don't exist as docfields but are used in onload
		"start": "ticket_date",
		"end": "ticket_date",
		"id": "name",
		"title": "ticket_title",
		"status": "status",
		"allDay": "allDay"
	},
	gantt: {
		"start": "ticket_date",
		"end": "ticket_date",
		"id": "name",
		"title": "ticket_title",
		"status": "status",
		"allDay": "allDay"
	},
	order_by: 'ticket_date',
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "category",
			"options": "Tickets Category",
			"label": __("Tickets Category")
		}
	],
	get_events_method: 'iac_helpdesk.iac_helpdesk.doctype.tickets.tickets.get_events'
}
