// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["On Time Delivery Report"] = {
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
			"fieldtype": "Select",
			"options": [
				{ "value": "All", "label": __("All") },
				{ "value": "Completed", "label": __("Completed") },
				{ "value": "To Deliver", "label": __("To Deliver") },
				{ "value": "To Deliver and Bill", "label": __("To Deliver and Bill") },
				{ "value": "To Bill", "label": __("To Bill") },
				{ "value": "Closed", "label": __("Closed") },
				{ "value": "Draft", "label": __("Draft") },
				{ "value": "Cancelled", "label": __("Cancelled") },
				
			],
			"default": "To Deliver and Bill"

					

                },

		{
                        "fieldname":"doc_status",
                        "label": __("Doc Status"),
			"fieldtype": "Select",
			"options": [
				{ "value": "0", "label": __("Draft") },
				{ "value": "1", "label": __("Submitted") },
				{ "value": "2", "label": __("Cancelled") },
								
			],
			"default": "1"

					

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

{
                        "fieldname":"cust_group",
                        "label": __("Customer Group"),
                        "fieldtype": "Link",
                        "options": "Customer Group"
                },
		
		
                                  
                
        ]
}

// $(function() {
//      $(wrapper).bind("show", function() {
//              frappe.query_report.load();
//      });
// });

