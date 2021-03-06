// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["Cost Center Verification Reports"] = {
	"filters": [
		
	        {
                        "fieldname":"cost_center",
                        "label": __("Cost Center"),
                        "fieldtype": "Link",
                        "options": "Cost Center",
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
               
	]
}
