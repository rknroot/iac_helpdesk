// Copyright (c) 2021, Eco Data & IAC and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recurrence Ticket Creation Tool', {
	refresh: function(frm) {
		frm.disable_save();
		frm.page.set_primary_action(__('Schedule Tickets'), () => {
			frm.call('schedule_ticket')
				.then(r => {
					if (!r.message) {
						frappe.throw(__('There were errors creating Tickets Schedule'));
					}
					const { tickets_schedule } = r.message;
					if (tickets_schedule) {
						const tickets_schedule_html = tickets_schedule.map(c => `
							<tr>
								<td><a href="/app/tickets/${c.name}">${c.name}</a></td>
								<td>${c.date}</td>
							</tr>
						`).join('');

						const html = `
							<table class="table table-bordered">
								<caption>${__('Following Tickets were created')}</caption>
								<thead><tr><th>${__("Tickets")}</th><th>${__("Date")}</th></tr></thead>
								<tbody>
									${tickets_schedule_html}
								</tbody>
							</table>
						`;

						frappe.msgprint(html);
					}
				});
		});
	}
});
