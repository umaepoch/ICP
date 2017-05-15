// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["Signages Pending Payments"] = {
	"filters": [

	 {
                        "fieldname":"name",
                        "label": __("Sales Invoice"),
                        "fieldtype": "Link",
                        "options": "Sales Invoice",
                        "reqd": 0
                },
                
                {      "fieldname":"from_date",
                        "label": __("From Date"),
                        "fieldtype": "Date",
                        "width": "80"
    //                    "default": sys_defaults.year_start_date,
                },
                {
                        "fieldname":"to_date",
                        "label": __("To Date"),
                        "fieldtype": "Date",
                        "width": "80"
     //                   "default": frappe.datetime.get_today()
                },
                {
                        "fieldname":"customer_group",
                        "label": __("Customer Group"),
                        "fieldtype": "Link",
                        "options": "Customer Group",
     //                   "default": frappe.datetime.get_today()
                },
	]
}
