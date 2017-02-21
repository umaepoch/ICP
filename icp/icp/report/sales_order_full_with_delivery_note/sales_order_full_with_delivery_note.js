// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order Full with Delivery Note"] = {
	"filters": [
		
		{
                        "fieldname":"assigned_to",
                        "label": __("Assigned To"),
                        "fieldtype": "Link",
			"options": "User",
                        "reqd": 0
                },
	        {
                        "fieldname":"name",
                        "label": __("Sales Order"),
                        "fieldtype": "Link",
                        "options": "Sales Order",
                        "reqd": 0
                },
                
                {      "fieldname":"from_date",
                        "label": __("Committed Delivery From Date"),
                        "fieldtype": "Date",
                        "width": "80"
    //                    "default": sys_defaults.year_start_date,
                },
                {
                        "fieldname":"to_date",
                        "label": __("Committed Delivery To Date"),
                        "fieldtype": "Date",
                        "width": "80"
     //                   "default": frappe.datetime.get_today()
                },
                {
                        "fieldname":"customer",
                        "label": __("Customer"),
                        "fieldtype": "Link",
                        "options": "Customer"
                },

		{
                        "fieldname":"so_status",
                        "label": __("Status"),
			"fieldtype": "Data",
                        "default": "To Deliver"
                },
		
                {
                        "fieldname":"item_code",
                        "label": __("Item"),
                        "fieldtype": "Link",
                        "options": "Item"
                },
		
		{
                        "fieldname":"item_group",
                        "label": __("Item Group"),
                        "fieldtype": "Link",
                        "options": "Item Group"
                },
		
		
                                  
                
        ]
}

// $(function() {
//      $(wrapper).bind("show", function() {
//              frappe.query_report.load();
//      });
// });

