// Copyright (c) 2021, Eco Data & IAC and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets', {
	refresh(frm)
	{
		$(cur_frm.fields_dict.create_ticket.input).addClass("btn-primary").css({'color':'white','font-weight': 'bold'});
	},
	/*onload(frm){
		if (frm.doc.create_recurrence_ticket == 1) {
			frm.doc.reload();
		}
	},*/
	create_ticket: function(frm){
		if (cur_frm.doc.__unsaved == 1) {
			frappe.throw('Save, to proceed!');
		} 
		else{
			frappe.call({
				method: 'iac_helpdesk.iac_helpdesk.doctype.tickets.tickets.get_tickets',
				args:{"start":frm.doc.ticket_date,
						"end": frm.doc.repeat_till,
						"user": frm.doc.name
				},
				callback: function(r){
					frappe.call({
						method: 'iac_helpdesk.iac_helpdesk.doctype.tickets.tickets.del_duplicate',
						args:{"start":frm.doc.ticket_date
						},
						callback: function(r){
							frappe.msgprint('Recurrence Tickets Created')
							frm.reload_doc()
						}	
					});
				}
			});
		}

	},
	repeat_on: function(frm) {
		if(frm.doc.repeat_on != "Weekly"){
			frm.doc.monday = '';
			frm.doc.tuesday = '';
			frm.doc.wednesday = '';
			frm.doc.thursday = '';
			frm.doc.friday = '';
			frm.doc.saturday = '';
			frm.doc.sunday = '';
			cur_frm.refresh_fields();
		}
	}
});
