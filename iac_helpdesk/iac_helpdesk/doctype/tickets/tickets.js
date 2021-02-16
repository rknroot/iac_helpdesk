// Copyright (c) 2021, Eco Data & IAC and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets', {
	validate(frm)
	{
		if(frm.doc.category == 'Cloud') {
			frm.doc.assigned_to = 'ca@dev.io';
		}
		else if (frm.doc.category == 'IT'){
			frm.doc.assigned_to = 'a@dev.io';
		}
	}

});
