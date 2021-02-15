frappe.views.calendar["Tickets"] = {
	field_map: {
		// from_datetime and to_datetime don't exist as docfields but are used in onload
		start: 'from_datetime',
		end: 'to_datetime',
		id: 'name',
		title: 'category',
		status: 'status',
		allDay: 'allDay'
	},
	gantt: false,
	order_by: 'date',
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
