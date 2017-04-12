// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["Salary List Report"] = {
	"filters": [

		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		}
	]
}
