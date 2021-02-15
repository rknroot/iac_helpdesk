/*
frappe.listview_settings['Tickets'] = {
    refresh(){
        if (frappe.user.has_role("Admin")) {
            if (!frappe.route_options) {
                frappe.route_options = {
                    "assigned_to": ["=",frappe.session.user]
                };
            }
        }
        if (frappe.user.has_role("Cloud Admin")) {
            if (!frappe.route_options) {
                frappe.route_options = {
                    "assigned_to": ["=",frappe.session.user]
                };
            }
        }
    },
    onload(){
        if (frappe.user.has_role("Cloud Admin")) {
            if (!frappe.route_options) {
                frappe.route_options = {
                    "assigned_to": ["=",frappe.session.user]
                };
            }
        }
        if (frappe.user.has_role("Admin")) {
            if (!frappe.route_options) {
                frappe.route_options = {
                    "assigned_to": ["=",frappe.session.user]
                };
            }
        }
    }
}*/