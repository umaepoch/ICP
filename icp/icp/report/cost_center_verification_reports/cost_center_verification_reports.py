# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, formatdate
from datetime import datetime, timedelta

def execute(filters=None):
        if not filters: filters = {}

        validate_filters(filters)

        columns = get_columns()
       
        item_map = get_item_details(filters)
        iwb_map = get_item_map(filters)

        data = []
        summ_data = [] 
	diff_data = 0	

        for (sales_invoice, item_code, income_account, cost_center) in sorted(iwb_map):
                qty_dict = iwb_map[(sales_invoice, item_code, income_account, cost_center)]
                data.append([
                        sales_invoice, item_code, income_account, cost_center, qty_dict.si_qty, qty_dict.amount, qty_dict.descr, qty_dict.created_date, qty_dict.modified_by, qty_dict.created_by
                        
                    ])

	for rows in data: 
		diff_data = 0

       		if 'Signage' in rows[2]:
			if 'Signage' in rows[3]:
				diff_data = 0
			else:
				diff_data = 1
		else:
			if 'FRP' in rows[2]:
				if 'FRP' in rows[3]:
					diff_data = 0
				else:
					diff_data = 1
		if diff_data == 1:		
								
			summ_data.append([rows[6], rows[0], rows[1],rows[2],
			 	rows[3], rows[4], rows[5], rows[9], rows[7], rows[8]
				
 				]) 
						 
	return columns, summ_data 


def get_columns():
        """return columns"""
               
        columns = [
		_("Type")+"::100",
		_("Invoice")+"::100",
		_("Item")+"::100",
		_("Income/Expense Account")+":Link/Account:150",
		_("Cost Center")+":Link/Cost Center:150",
		_("Qty")+"::100",
		_("Amount")+":Int:100",
		_("Created By")+"::100",
		_("Creation Date")+":Date:100",
		_("Modified By")+"::100",
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

             
        if filters.get("name"):
                conditions += " and si.parent = '%s'" % frappe.db.escape(filters.get("name"), percent=False)

	
        return conditions

def get_cost_details_sales(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select si.parent as sales_invoice, si.item_code as item_code, si.income_account as income_account, si.cost_center, si.qty as qty, si.amount as amount, so.creation as created_date, so.owner as created_by, so.modified_by as modified_by, "Sales Invoice" as descr 
                from `tabSales Invoice Item` si, `tabSales Invoice` so
                where so.name = si.parent and so.status != "Cancelled" %s order by si.parent, si.item_code""" % conditions, as_dict=1)

def get_cost_details_purchase(filters):
        conditions = get_conditions(filters)

#	if not (conditions):	
	return frappe.db.sql("""select pi.parent as sales_invoice, pi.item_code as item_code, pi.expense_account as income_account, pi.cost_center, pi.qty as qty, pi.amount as amount, po.creation as created_date, po.owner as created_by, po.modified_by as modified_by, "Purchase Invoice" as descr
                from `tabPurchase Invoice Item` pi, `tabPurchase Invoice` po
                where po.name = pi.parent and po.status != "Cancelled" %s order by pi.parent, pi.item_code""" % conditions, as_dict=1)

def get_cost_details_del(filters):
        conditions = get_conditions(filters)

#	if not (conditions):	
	return frappe.db.sql("""select di.parent as sales_invoice, di.item_code as item_code, di.expense_account as income_account, di.cost_center, di.qty as qty, di.amount as amount, do.creation as created_date, do.owner as created_by, do.modified_by as modified_by, "Delivery Note" as descr
                from `tabDelivery Note Item` di, `tabDelivery Note` do
                where do.name = di.parent and do.status != "Cancelled" %s order by di.parent, di.item_code""" % conditions, as_dict=1)

def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
 #       to_date = getdate(filters["to_date"])
	
        sle = get_cost_details_sales(filters)
        dle = get_cost_details_purchase(filters)
        kle = get_cost_details_del(filters)

        for d in sle:
                
                key = (d.sales_invoice, d.item_code, d.income_account, d.cost_center)
                if key not in iwb_map:
                        iwb_map[key] = frappe._dict({
                                "si_qty": 0.0,
				"amount": 0.0,
				"descr": " "
                        })

                qty_dict = iwb_map[(d.sales_invoice, d.item_code, d.income_account, d.cost_center)]

                
                qty_dict.si_qty = d.qty
		qty_dict.amount = d.amount
		qty_dict.descr = d.descr
		qty_dict.created_date = d.created_date
		qty_dict.created_by = d.created_by
		qty_dict.modified_by = d.modified_by
		
        if dle:
		for d in dle:
			key = (d.sales_invoice, d.item_code, d.income_account, d.cost_center)
                	if key not in iwb_map:
                        	iwb_map[key] = frappe._dict({
                        	        "si_qty": 0.0,
					"amount": 0.0,
					"descr": " "
                        	})

	                qty_dict = iwb_map[(d.sales_invoice, d.item_code, d.income_account, d.cost_center)]

        	        
        	        qty_dict.si_qty = d.qty
			qty_dict.amount = d.amount
			qty_dict.descr = d.descr
			qty_dict.created_date = d.created_date
			qty_dict.created_by = d.created_by
			qty_dict.modified_by = d.modified_by

        if kle:
		for d in kle:
			key = (d.sales_invoice, d.item_code, d.income_account, d.cost_center)
                	if key not in iwb_map:
                        	iwb_map[key] = frappe._dict({
                        	        "si_qty": 0.0,
					"amount": 0.0,
					"descr": " "
                        	})

	                qty_dict = iwb_map[(d.sales_invoice, d.item_code, d.income_account, d.cost_center)]

        	        
        	        qty_dict.si_qty = d.qty
			qty_dict.amount = d.amount
			qty_dict.descr = d.descr
			qty_dict.created_date = d.created_date
			qty_dict.created_by = d.created_by	
			qty_dict.modified_by = d.modified_by

        return iwb_map

def get_item_details(filters):
        condition = ''
        value = ()
        if filters.get("item_code"):
                condition = "where item_code=%s"
                value = (filters["item_code"],)
	
        items = frappe.db.sql("""select item_group, item_name, stock_uom, name, brand, description
                from tabItem {condition}""".format(condition=condition), value, as_dict=1)

        return dict((d.name, d) for d in items)

def validate_filters(filters):
        if not (filters.get("item_code") or filters.get("warehouse")):
                sle_count = flt(frappe.db.sql("""select count(name) from `tabSales Invoice Item`""")[0][0])
                if sle_count > 500000:
                        frappe.throw(_("Please set filter based on Item or Warehouse"))



