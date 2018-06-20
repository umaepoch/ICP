// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Order Items To Be Received ICP"] = {
	"filters": [
                 {
                        "fieldname":"po_series",
                        "label": __("Purchase Order Series"),
                        "fieldtype": "Select",
			"options": [
				{ "value": "PO-", "label": __("PO-") },
				{ "value": "PO/U1/18-19/", "label": __("PO/U1/18-19/") },
				{ "value": "PO/U2/18-19/", "label": __("PO/U2/18-19/") },
				{ "value": "JO/18-19/", "label": __("JO/18-19/") },
				{ "value": "TPT/18-19/", "label": __("TPT/18-19/") },
				{ "value": "PO/U1/17-18/", "label": __("PO/U1/17-18/") },
				{ "value": "PO/U2/17-18/", "label": __("PO/U2/17-18/") },
				{ "value": "JO/17-18/", "label": __("JO/17-18/") },
				{ "value": "TPT/17-18/", "label": __("TPT/17-18/") },
				
			],
			"default": "PO/U1/18-19/",

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
                        "fieldname":"supplier",
                        "label": __("Supplier"),
                        "fieldtype": "Link",
                        "options": "Supplier"
                }

         
	]
}
