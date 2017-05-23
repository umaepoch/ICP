# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, formatdate
from datetime import datetime, timedelta

def execute(filters=None):
        if not filters: filters = {}

       
        columns = get_columns()
       
        iwb_map = get_item_map(filters)

        data = []
        summ_data = [] 
	diff_data = 0	

        for (sales_invoice) in sorted(iwb_map):
                qty_dict = iwb_map[(sales_invoice)]


                data.append([sales_invoice, qty_dict.customer, qty_dict.customer_group, qty_dict.posting_date, qty_dict.buyers_order_ref, qty_dict.delivery_at, qty_dict.out_amt, qty_dict.due_date, qty_dict.submitted_to_customer, qty_dict.payment_follow])

	for rows in data: 
		diff_data = 0

       		if 'Petroleum' in rows[1]:
			diff_data = 1
		else:
			if 'Indian Oil' in rows[1]:
				diff_data = 1
			else:
				diff_data = 0
		if diff_data == 1:		
								
			summ_data.append([rows[0], rows[1], rows[2],
			 	rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9]				
 				]) 
						 
	return columns, summ_data 


def get_columns():
        """return columns"""
               
        columns = [
		_("Invoice")+":Link/Sales Invoice:100",
		_("Customer")+"::100",
		_("Customer Group")+"::100",
		_("Posting Date")+":Date:100",
		_("Buyers Order Ref")+"::150",
		_("Delivery At")+"::100",
		_("Outstanding Amount")+":Int:100",
		_("Due Date")+":Date:100",
		_("Submitted to Customer")+"::100",
		_("Payment Follow Up Notes")+"::100",
         ]

        return columns

def get_conditions(filters):
        conditions = ""
        if filters.get("from_date"):
		conditions += " and inv.delivery_date >= '%s'" % frappe.db.escape(filters["from_date"])
 #       else:
#		frappe.throw(_("'From Date' is required"))	

        if filters.get("to_date"):
                conditions += " and inv.delivery_date <= '%s'" % frappe.db.escape(filters["to_date"])
#        else:
 #               frappe.throw(_("'To Date' is required"))

             
        if filters.get("name"):
                conditions += " and inv.name = '%s'" % frappe.db.escape(filters.get("name"), percent=False)

	
        return conditions

def get_sales_details(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select inv.name as sales_invoice, inv.customer, inv.customer_group, inv.posting_date, inv.buyers_order_ref, inv.delivery_at, inv.outstanding_amount, inv.due_date, inv.submitted_to_customer, inv.payment_followup_notes
                from `tabSales Invoice` inv
		where (inv.customer_group = "Signages" or inv.customer_group = "Commercial") and inv.outstanding_amount > 0 %s
		order by inv.customer, inv.posting_date""" % conditions, as_dict=1)


def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
 #       to_date = getdate(filters["to_date"])
	
        sle = get_sales_details(filters)

        for d in sle:
                
                key = (d.sales_invoice)
                if key not in iwb_map:
                        iwb_map[key] = frappe._dict({
                                "out_amt": 0.0,
				
                        })

                qty_dict = iwb_map[(d.sales_invoice)]

                
                qty_dict.sales_invoice = d.sales_invoice
		qty_dict.customer = d.customer
		qty_dict.cust_group = d.customer_group
		qty_dict.posting_date = d.posting_date
		qty_dict.buyers_order_ref = d.buyers_order_ref
		qty_dict.delivery_at = d.delivery_at
		qty_dict.out_amt = d.outstanding_amount
		qty_dict.due_date = d.due_date
		qty_dict.submitted_to_customer = d.submitted_to_customer
		qty_dict.payment_follow = d.payment_followup_notes
		
      
        return iwb_map



