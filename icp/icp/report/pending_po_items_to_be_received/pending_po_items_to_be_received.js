// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pending PO Items to be Received"] = {
	"filters": [

	
		
                {      "fieldname":"from_date",
                        "label": __("Pending POs From Date"),
                        "fieldtype": "Date",
                        "width": "80",
			"reqd": 1,
                        "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
                },
                {
                        "fieldname":"to_date",
                        "label": __("Pending POs To Date"),
                        "fieldtype": "Date",
                        "width": "80",
			"reqd":1,
                        "default": frappe.datetime.get_today()
                },

		 {      "fieldname":"supplier",
                        "label": __("Supplier"),
                        "fieldtype": "Link",
			"options": "Supplier",
                        "width": "80",
			"reqd": 0
                },
                      
		 {      "fieldname":"series",
                        "label": __("Naming Series"),
                        "fieldtype": "Select",
			"options": [{"value": "PO/U1/17-18/"}, {"value": "PO/U2/17-18/"}, {"value": "JO/17-18/"}, {"value":"TPT/17-18/"}, {"value":"PO/U1/18-19/"}, {"value":"PO/U2/18-19/"},
				{"value":"JO/18-19/"}, {"value":"TPT/18-19/"}, {"value":"PO/U1/16-17/"}, {"value":"PO/U2/16-17/"}, {"value":"JO/16-17/"}, {"value":"TPT/16-17/"}, {"value":"PO/15-16/"},
				{"value":"JO/15-16/"}, {"value":"TPT/15-16/"}, {"value":"PO/14-15/"}],
                        "width": "80",
			"reqd": 0
                }
            
                
        ]
}


