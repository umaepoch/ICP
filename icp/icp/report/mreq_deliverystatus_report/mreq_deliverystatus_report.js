// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["Mreq-DeliveryStatus Report"] = {
	"filters": [

	
		{
                        "fieldname":"requested_by",
                        "label": __("Requested By"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Basavaraj", "label": __("Basavaraj") },
				{ "value": "Nataraju", "label": __("Nataraju") },
				{ "value": "Manjunath", "label": __("Manjunath") },
				{ "value": "Siddaraju", "label": __("Siddaraju") },
				{ "value": "Vaitheeswaran", "label": __("Vaitheeswaran") },
				{ "value": "Ranganathappa", "label": __("Ranganathappa") },
				{ "value": "Shivakumar", "label": __("Shivakumar") },
				{ "value": "Suresh", "label": __("Suresh") }
				
			],
			"default": ""
                }		
                                  
                
        ]
}


