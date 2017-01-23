// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order Full with Delivery Note"] = {
	"filters": [
		
		{
                        "fieldname":"assigned_to",
                        "label": __("Assigned To"),
                        "fieldtype": "Data",
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
                        "fieldname":"warehouse",
                        "label": __("Warehouse"),
                        "fieldtype": "Link",
                        "options": "Warehouse"
                },
                {
                        "fieldname":"item_code",
                        "label": __("Item"),
                        "fieldtype": "Link",
                        "options": "Item"
                },
		{
                        "fieldname":"brand",
                        "label": __("Brand"),
                        "fieldtype": "Link",
                        "options": "Brand"
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

