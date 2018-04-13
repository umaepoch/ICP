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
        summ_data = [] 
	diff_days = 0
	curr_date = utils.today()
	temp_date = getdate("2001-01-01")
		

        for (sales_order, item_code) in sorted(iwb_map):
                qty_dict = iwb_map[(sales_order, item_code)]
		if qty_dict.item_del_date == " ":
			diff_days = 0
		else:
			diff_days = getdate(curr_date) - getdate(qty_dict.item_del_date)

                data.append([qty_dict.assigned_to, sales_order, qty_dict.customer, qty_dict.po_no, qty_dict.trans_date, item_code,  qty_dict.description, qty_dict.item_del_date, diff_days, qty_dict.qty, qty_dict.delivered_qty, qty_dict.qty_to_deliver, qty_dict.rate, qty_dict.amount_to_deliver, qty_dict.item_group ])
						 
	return columns, data 


def get_columns():
        """return columns"""
               
        columns = [
		_("Assigned To")+"::50",
		_("Sales Order")+":Link/Sales Order:125",
		_("Customer")+":Link/Customer:80",
		_("PO Number")+"::30",
		_("Date")+":Date:80",
		_("Item")+":Link/Item:80",
		_("Description")+"::100",
		_("Item Delivery Date")+":Date:80",
		_("Delay Days")+":Int:50",
		_("Qty")+":Int:50",
		_("Delivered Qty")+":Int:50",
		_("Qty to Deliver")+":Int:50",
		_("Rate")+":Int:60",
		_("Amount to Deliver")+":Int:60",
		_("Item Group")+":Link/Item Group:50"
         ]

        return columns

def get_conditions(filters):
        conditions = ""
        if filters.get("from_date"):
		conditions += " and so.delivery_date >= '%s'" % frappe.db.escape(filters["from_date"])
 #       else:
#		frappe.throw(_("'From Date' is required"))	

        if filters.get("to_date"):
                conditions += " and so.delivery_date <= '%s'" % frappe.db.escape(filters["to_date"])
#        else:
 #               frappe.throw(_("'To Date' is required"))

        if filters.get("item_code"):
                conditions += " and si.item_code = '%s'" % frappe.db.escape(filters.get("item_code"), percent=False)
	
	if filters.get("assigned_to"):
		pre_ass = '["'
		suf_ass = '"]'
		assign_to = pre_ass + filters.get("assigned_to") + suf_ass 
		conditions += " and so._assign = '%s'" % assign_to
     
        if filters.get("name"):
                conditions += " and si.parent = '%s'" % frappe.db.escape(filters.get("name"), percent=False)

	
	if filters.get("item_group"):
                conditions += " and si.item_group = '%s'" % frappe.db.escape(filters.get("item_group"), percent=False)
	
	if filters.get("cust_group"):
                conditions += " and so.customer_group = '%s'" % frappe.db.escape(filters.get("cust_group"), percent=False)

        if filters.get("customer"):
                conditions += " and so.customer = '%s'" % frappe.db.escape(filters.get("customer"), percent=False)

	return conditions


def get_sales_details(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select so._assign as assigned_to, so.name as sales_order, so.customer as customer, so.customer_name as customer_name, so.po_no as po_no, so.transaction_date as trans_date, si.item_code as item_code, si.description as description, si.qty as qty, si.delivered_qty as delivered_qty, (si.qty - si.delivered_qty) as qty_to_deliver, si.base_rate as rate, si.base_amount as amount, ((si.qty - si.delivered_qty) * si.base_rate) as amount_to_deliver, si.delivery_date as item_del_date, si.item_group as item_group
from
 `tabSales Order` so, `tabSales Order Item` si
where
 si.parent = so.name
 and so.docstatus = 1
 and so.status not in ("Stopped", "Closed")
 and si.delivered_qty < si.qty %s
order by so.transaction_date asc""" % conditions, as_dict=1)


def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
 #       to_date = getdate(filters["to_date"])
	
        sle = get_sales_details(filters)

        for d in sle:
                
                key = (d.sales_order, d.item_code)
                if key not in iwb_map:
                        iwb_map[key] = frappe._dict({
                                "out_amt": 0.0,
				
                        })

                qty_dict = iwb_map[(d.sales_order, d.item_code)]

	        qty_dict.assigned_to = d.assigned_to
	        qty_dict.sales_order = d.sales_order
		qty_dict.customer = d.customer
		qty_dict.customer_name = d.customer_name
		qty_dict.po_no = d.po_no
		qty_dict.trans_date = d.trans_date
		qty_dict.description = d.description
		qty_dict.qty = d.qty
		qty_dict.delivered_qty = d.delivered_qty
		qty_dict.qty_to_deliver = d.qty_to_deliver
		qty_dict.rate = d.rate
		qty_dict.amount = d.amount
		qty_dict.amount_to_deliver = d.amount_to_deliver
		qty_dict.item_del_date = d.item_del_date
		qty_dict.item_group = d.item_group

		
      
        return iwb_map



