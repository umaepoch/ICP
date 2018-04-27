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
                        material_request, qty_dict.transaction_date, qty_dict.modifed_by, qty_dict.requested_by, qty_dict.status, purchase_order, item_code, qty_dict.description, qty_dict.expected_delivery_date, qty_dict.revised_delivery_date, qty_dict.req_qty, qty_dict.qty, qty_dict.received_qty, qty_dict.per_received
                        
                    ])
						 
	return columns, data 


def get_columns():
        """return columns"""
               
        columns = [

		_("Material Request")+"::150",
                _("Transaction Date")+":Date:100",
		_("Modified By")+"::150",
		_("Requested By")+"::140",
		_("Status")+"::100",
		_("Linked PO")+"::150",
		_("Item Code")+"::100",
		_("Description")+"::100",
		_("Required By Date from Purchase Order Item")+"::100",
                _("Updated Delivery Date")+":Date:100",
		_("Requested Qty")+"::100",
		_("Ordered Qty")+"::100",
	        _("Received Qty")+"::100",
		_("Percentage Received")+":Float:100"
       	       
          ]

        return columns

def get_conditions(filters):
        conditions = ""
        
        if filters.get("requested_by"):

		conditions += " and mr.requested_by = '%s'" % filters.get("requested_by")

        if filters.get("from_date"):
		conditions += " and mr.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
 #       else:
#		frappe.throw(_("'From Date' is required"))	

        if filters.get("to_date"):
                conditions += " and mr.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])


        return conditions

def get_mr_details(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select pi.material_request as material_request, mr.transaction_date as transaction_date, mr.modified_by, mr.requested_by, mr.status, mr.docstatus, pi.parent as purchase_order, pi.item_code as item_code, pi.description as description, pi.schedule_date as expected_delivery_date, pi.revised_delivery_date as revised_delivery_date, mri.qty as req_qty, pi.qty as pi_qty, pi.received_qty as received_qty, (pi.received_qty/pi.qty*100) as per_received from `tabPurchase Order Item` pi, `tabMaterial Request` mr, `tabMaterial Request Item` mri where mr.name = mri.parent and pi.material_request = mr.name and mr.docstatus = "1" and pi.docstatus != "2" %s order by pi.material_request""" % conditions, as_dict=1)

def get_mr_wo_po(filters):
        conditions = get_conditions(filters)
 
	return frappe.db.sql("""select mr.name as material_request, mr.transaction_date as transaction_date, mr.modified_by, mr.requested_by, mr.status, mr.docstatus, "" as purchase_order, mri.item_code as item_code, mri.description as description, "" as expected_delivery_date, "" as revised_delivery_date, mri.qty as req_qty, 0 as pi_qty, 0 as received_qty, 0 as per_received from `tabMaterial Request` mr, `tabMaterial Request Item` mri where mr.name = mri.parent and mr.docstatus = "1" %s and not exists (
                select 1 from `tabPurchase Order Item` pi, `tabMaterial Request Item` mr1 where pi.material_request = mr1.name) order by mr.name""" % conditions, as_dict=1)

def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
#        to_date = getdate(filters["to_date"])
	
        sle = get_mr_details(filters)
	ple = get_mr_wo_po(filters)
		
        if sle:     	
	        for d in sle:
                
        	        key = (d.material_request, d.purchase_order, d.item_code)
        	        iwb_map[key] = frappe._dict({
        	                 "qty": 0.0, "value": 0.0,				
        	        })

        	        qty_dict = iwb_map[(d.material_request, d.purchase_order, d.item_code)]

        	        qty_dict.modifed_by = d.modified_by
			qty_dict.transaction_date = d.transaction_date
	                qty_dict.requested_by = d.requested_by
	                qty_dict.status = d.status
			qty_dict.docstatus = d.docstatus
			qty_dict.description = d.description
			qty_dict.expected_delivery_date = d.expected_delivery_date
			qty_dict.revised_delivery_date = d.revised_delivery_date
			qty_dict.req_qty = d.req_qty
			qty_dict.qty = d.pi_qty
			qty_dict.received_qty = d.received_qty
			qty_dict.per_received = d.per_received

        if ple:     	
	        for d in ple:
                
        	        key = (d.material_request, d.purchase_order, d.item_code)
        	        iwb_map[key] = frappe._dict({
        	                 "qty": 0.0, "value": 0.0,				
        	        })

        	        qty_dict = iwb_map[(d.material_request, d.purchase_order, d.item_code)]

        	        qty_dict.modifed_by = d.modified_by
			qty_dict.transaction_date = d.transaction_date
	                qty_dict.requested_by = d.requested_by
	                qty_dict.status = d.status
			qty_dict.docstatus = d.docstatus
			qty_dict.description = d.description
			qty_dict.expected_delivery_date = d.expected_delivery_date
			qty_dict.revised_delivery_date = d.revised_delivery_date
			qty_dict.req_qty = d.req_qty
			qty_dict.qty = d.pi_qty
			qty_dict.received_qty = d.received_qty
			qty_dict.per_received = d.per_received


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



