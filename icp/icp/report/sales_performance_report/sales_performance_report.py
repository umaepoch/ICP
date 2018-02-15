# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, utils
from frappe.utils import flt, getdate, formatdate
from datetime import datetime, timedelta

def execute(filters=None):
        if not filters: filters = {}

       
        columns = get_columns()
       
        iwb_map = get_item_map(filters)

        data = []
		

        for (sales_invoice, sales_order) in sorted(iwb_map):
                qty_dict = iwb_map[(sales_invoice, sales_order)]

                data.append([sales_invoice, qty_dict.date, qty_dict.customer, qty_dict.buyers_order_ref, qty_dict.delivery_at, qty_dict.total, qty_dict.sales_order, qty_dict.assigned_to ])
						 
	return columns, data 


def get_columns():
        """return columns"""
               
        columns = [
		_("Sales Invoice #")+":Link/Sales Invoice:120",
		_("Date")+":Date:80",
		_("Customer Name")+":Link/Customer:110",
		_("Buyer Order No.")+"::110",
		_("Delivery at")+"::120",
		_("Net Total")+":Float:100",
		_("Sales Order#")+":Link/Sales Order:130",
		_("Assigned To")+"::100",
         ]

        return columns

def get_conditions(filters):
        conditions = ""
        if filters.get("from_date"):
		conditions += " and si.delivery_date >= '%s'" % frappe.db.escape(filters["from_date"])
 #       else:
#		frappe.throw(_("'From Date' is required"))	

        if filters.get("to_date"):
                conditions += " and si.delivery_date <= '%s'" % frappe.db.escape(filters["to_date"])
#        else:
 #               frappe.throw(_("'To Date' is required"))

	
	if filters.get("assigned_to"):
		pre_ass = '["'
		suf_ass = '"]'
		assign_to = pre_ass + filters.get("assigned_to") + suf_ass 
		conditions += " and so._assign = '%s'" % assign_to
     
	
	if filters.get("cust_group"):
                conditions += " and si.customer_group = '%s'" % frappe.db.escape(filters.get("cust_group"), percent=False)

        if filters.get("customer"):
                conditions += " and si.customer = '%s'" % frappe.db.escape(filters.get("customer"), percent=False)

	return conditions


def get_sales_details(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select sl.name as sales_invoice, so._assign as assigned_to, sl.posting_date as date, sl.customer as customer, sl.buyers_order_ref, sl.delivery_at as delivery_at, sl.net_total as total, so.name as sales_order
                from `tabSales Invoice Item` sli, `tabSales Invoice` sl, `tabSales Order Item` si, `tabSales Order` so
                where so.name = si.parent and sl.name = sli.parent and sli.sales_order = so.name %s order by sl.name, sl.posting_date asc""" % conditions, as_dict=1)



def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
 #       to_date = getdate(filters["to_date"])
	
        sle = get_sales_details(filters)

        for d in sle:
                
                key = (d.sales_invoice, d.sales_order)
                if key not in iwb_map:
                        iwb_map[key] = frappe._dict({
                                "total": 0.0,
				
                        })

                qty_dict = iwb_map[(d.sales_invoice, d.sales_order)]

	        qty_dict.assigned_to = d.assigned_to
	        qty_dict.sales_order = d.sales_order
		qty_dict.customer = d.customer
		qty_dict.date = d.date
		qty_dict.buyers_order_ref = d.buyers_order_ref
		qty_dict.delivery_at = d.delivery_at
		qty_dict.total = d.total
		
      
        return iwb_map



