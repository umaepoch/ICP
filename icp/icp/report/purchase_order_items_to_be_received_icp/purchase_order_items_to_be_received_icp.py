# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate

def execute(filters=None):
        if not filters: filters = {}

        validate_filters(filters)

        columns = get_columns()
       
        item_map = get_item_details(filters)
        iwb_map = get_item_map(filters)

        data = []
         	        
        for (material_request, purchase_order, item_code) in sorted(iwb_map):
                qty_dict = iwb_map[(material_request, purchase_order, item_code)]
                data.append([
                        material_request, qty_dict.transaction_date, qty_dict.requested_by, purchase_order, qty_dict.po_date, qty_dict.reqd_by_date, qty_dict.edd, qty_dict.supplier_name, item_code, qty_dict.description, qty_dict.uom, qty_dict.qty, qty_dict.received_qty, qty_dict.qty_to_receive
                        
                    ])
						 
	return columns, data 


def get_columns():
        """return columns"""
               
        columns = [

		_("Material Request")+"::150",
                _("Material Request Date")+":Date:100",
		_("Requested For")+"::140",
		_("Purchase Order")+"::140",
		_("PO Date")+"::140",
		_("Reqd by Date")+"::100",
		_("Expected Delivery Date")+":Date:100",
		_("Supplier Name")+"::140",
		_("Item Code")+"::100",
		_("Description")+"::100",
		_("UOM")+"::100",
		_("Qty")+"::100",
	        _("Received Qty")+"::100",
		_("Qty to Receive")+":Float:100"
       	       
          ]

        return columns

def get_conditions(filters):
        conditions = ""
        
        if filters.get("po_series"):
		conditions += " and po.naming_series = '%s'" % filters.get("po_series")

        if filters.get("requested_by"):
		conditions += " and mr.requested_by = '%s'" % filters.get("requested_by")

        if filters.get("from_date"):
		conditions += " and mr.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
 #       else:
#		frappe.throw(_("'From Date' is required"))	

        if filters.get("to_date"):
                conditions += " and mr.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])
        
	if filters.get("supplier"):
		conditions += " and po.supplier = '%s'" % filters.get("supplier")


        return conditions

def get_mr_details(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select mr.name as material_request, mr.transaction_date as transaction_date, mr.requested_by as requested_by, po.name as purchase_order, po.transaction_date as po_date, pi.schedule_date as reqd_by_date, pi.expected_delivery_date as edd, po.supplier as supplier_name, pi.item_code as item_code, pi.description as description, pi.uom as uom, pi.qty as qty, pi.received_qty as received_qty, (pi.qty - ifnull(pi.received_qty, 0)) as qty_to_receive
    
from
	`tabPurchase Order` po JOIN `tabPurchase Order Item` pi
         LEFT JOIN `tabMaterial Request` mr ON (mr.name = pi.material_request)
where
	pi.parent = po.name
	and po.docstatus = 1
	and po.status not in ("Stopped", "Closed")
	and ifnull(pi.received_qty, 0) < ifnull(pi.qty, 0) %s
order by po.transaction_date asc

""" % conditions, as_dict=1)


def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
#        to_date = getdate(filters["to_date"])
	
        sle = get_mr_details(filters)
		
        if sle:     	
	        for d in sle:
                
        	        key = (d.material_request, d.purchase_order, d.item_code)
        	        iwb_map[key] = frappe._dict({
        	                 "qty": 0.0, "value": 0.0,				
        	        })

        	        qty_dict = iwb_map[(d.material_request, d.purchase_order, d.item_code)]

			qty_dict.transaction_date = d.transaction_date
	                qty_dict.requested_by = d.requested_by
	                qty_dict.po_date = d.po_date
			qty_dict.reqd_by_date = d.reqd_by_date
			qty_dict.edd = d.edd
			qty_dict.supplier_name = d.supplier_name
			qty_dict.description = d.description
			qty_dict.received_qty = d.received_qty
			qty_dict.qty = d.pi_qty
			qty_dict.qty_to_receive = d.qty_to_receive
			qty_dict.uom = d.uom


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
                sle_count = flt(frappe.db.sql("""select count(name) from `tabStock Ledger Entry`""")[0][0])
                if sle_count > 500000:
                        frappe.throw(_("Please set filter based on Item or Warehouse"))



