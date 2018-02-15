// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Performance Report"] = {
	
	"filters": [
	
		
                
                {      "fieldname":"from_date",
                        "label": __("Invoice Date Start"),
                        "fieldtype": "Date",
                        "width": "80",
			"reqd": 1,
                },

                {
                        "fieldname":"to_date",
                        "label": __("Invoice Date End"),
                        "fieldtype": "Date",
                        "width": "80",
			"reqd": 1,
                        "default": frappe.datetime.get_today()
                },


		{
                        "fieldname":"assigned_to",
                        "label": __("Assigned To"),
                        "fieldtype": "Link",
			"options": "User",
                        "reqd": 0
                },
                {
                        "fieldname":"customer",
                        "label": __("Customer"),
                        "fieldtype": "Link",
                        "options": "Customer"
                },

		{
                        "fieldname":"cust_group",
                        "label": __("Customer Group"),
                        "fieldtype": "Link",
                        "options": "Customer Group"
			
                }
                                
  ]
}


