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
		

        for (purchase_order, item_name) in sorted(iwb_map):
                qty_dict = iwb_map[(purchase_order, item_name)]

                data.append([purchase_order, qty_dict.transaction_date, qty_dict.schedule_date, qty_dict.supplier, qty_dict.qty, qty_dict.recd_qty, (qty_dict.qty - qty_dict.recd_qty), qty_dict.item_name, qty_dict.description ])

						 
	return columns, data 


def get_columns():
        """return columns"""
               
        columns = [
		_("Purchase Order")+"::80",		
		_("Date")+":Date:80",
		_("Reqd By Date")+":Date:80",
		_("Supplier Name")+":Link/Customer:110",
		_("Qty")+"::110",
		_("Qty to Receive")+"::110",
		_("Received Qty")+"::120",
		_("Item Name")+"::130",
		_("Description")+"::100"
         ]

        return columns

def get_conditions(filters):
        conditions = ""
        if filters.get("from_date"):
		conditions += " and po.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
 #       else:
#		frappe.throw(_("'From Date' is required"))	

        if filters.get("to_date"):
                conditions += " and po.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])
#        else:
 #               frappe.throw(_("'To Date' is required"))
   
	
	if filters.get("supplier"):
                conditions += " and po.supplier = '%s'" % frappe.db.escape(filters.get("supplier"), percent=False)

        if filters.get("series"):
                conditions += " and po.naming_series = '%s'" % frappe.db.escape(filters.get("series"), percent=False)

	return conditions


def get_po_details(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select po.name as purchase_order, po.transaction_date as transaction_date, pi.schedule_date as reqd_date, 
			pi.item_name as item_name, pi.qty as qty, pi.description as description, po.supplier as supplier, pi.received_qty as 				recd_qty from `tabPurchase Order` po, `tabPurchase Order Item` pi
			where po.name = pi.parent %s order by po.name, po.transaction_date asc""" % conditions, as_dict=1)


def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
 #       to_date = getdate(filters["to_date"])
	
        sle = get_po_details(filters)

        for d in sle:
                
                key = (d.purchase_order, d.item_name)
                if key not in iwb_map:
                        iwb_map[key] = frappe._dict({
                                "qty": 0,
				"received_qty": 0
				
                        })

                qty_dict = iwb_map[(d.purchase_order, d.item_name)]

	        qty_dict.purchase_order = d.purchase_order
	        qty_dict.transaction_date = d.transaction_date
		qty_dict.schedule_date = d.schedule_date
		qty_dict.item_name = d.item_name
		qty_dict.qty = d.qty
		qty_dict.recd_qty = d.recd_qty
		qty_dict.description = d.description
		qty_dict.supplier = d.supplier
		
      
        return iwb_map



