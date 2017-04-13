# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, datetime

def execute(filters=None):
        if not filters: filters = {}

        validate_filters(filters)

        columns = get_columns()
        item_map = get_item_details(filters)
        iwb_map = get_item_warehouse_map(filters)

        data = []
        summ_data = [] 
        so_prev = "" 
        so_work = "" 
        so_count = 0 
        tot_bal_qty = 0 

        tot_bi_qty = 0
	tot_si_qty = 0
        
	for (sales_order, bom, item, whse) in sorted(iwb_map):
                qty_dict = iwb_map[(sales_order, bom, item, whse)]
                data.append([
                        sales_order, item, qty_dict.si_qty, bom, qty_dict.bi_item, item_map[item]["description"],
                        item_map[item]["item_group"],
                        item_map[item]["item_name"], 
                        item_map[item]["stock_uom"], 
                        qty_dict.bal_qty, qty_dict.bi_qty, whse,                                              
                        item_map[item]["brand"]
                    ])

       		
	for rows in data: 

		if so_count == 0: 

       			so_prev = rows[0] 

	                tot_bal_qty = tot_bal_qty + rows[9] 
			tot_bi_qty = tot_bi_qty + rows[10]
                        summ_data.append([so_prev, rows[1], rows[2],
		 	rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[10],
			rows[9], rows[11]
 			]) 
                else: 
			so_work = rows[0] 

			if so_prev == so_work: 

				tot_bal_qty = tot_bal_qty + rows[9] 
				
				tot_bi_qty = tot_bi_qty + rows[10]
        	                summ_data.append([so_prev, rows[1], rows[2],
		 	rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[10],
			rows[9], rows[11]			 
 				]) 
			else: 

				summ_data.append([so_prev, " ", " ", " ", " ", " ", 
			 	" ", " ", " ", tot_bi_qty,
				tot_bal_qty, " ", " "
 				])				 

				summ_data.append([so_work,rows[1], rows[2],
		 	rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[10],
			rows[9], rows[11]
 				]) 
        	                        
				tot_bal_qty = 0 
 
 				tot_bi_qty = 0
        	                tot_bal_qty = tot_bal_qty + rows[9] 
				
				tot_bi_qty = tot_bi_qty + rows[10] 
				so_prev = so_work 
                               
		so_count = so_count + 1 
	summ_data.append([so_prev, " ", " ", " ", " ", " ",
		" ", " ", " ", tot_bi_qty,
		tot_bal_qty, " ", " "
 		])	 

						 
	return columns, summ_data 



def get_columns():
        """return columns"""
        columns = [
		_("Sales Order")+":Link/Sales Order:100",
		_("Sales Order Item")+":Link/Item:100",
		_("SO Qty")+":Float:100",
		_("BOM")+":Link/BOM:100",
                _("Item")+":Link/Item:100",
                _("Description")+"::140",
                _("Item Group")+"::100",
                _("Item Name")+"::150",
 #               _("Warehouse")+":Link/Warehouse:100",
                _("Stock UOM")+":Link/UOM:90",
		_("BoM Qty")+":Float:100",
                _("Balance Qty")+":Float:100",
                _("Warehouse")+"::100",
                _("Brand")+"::100"

              
         ]

        return columns

def get_conditions(filters):
        conditions = ""
	
	if filters.get("company"):
                conditions += " and so.company = '%s'" % frappe.db.escape(filters.get("company"), percent=False)

        if filters.get("item_code"):
                conditions += " and item_code = '%s'" % frappe.db.escape(filters.get("item_code"), percent=False)
     
        if filters.get("bom"):
                conditions += " and bi.parent = '%s'" % frappe.db.escape(filters.get("bom"), percent=False)
	if filters.get("sales_order"):
                conditions += " and si.parent = '%s'" % frappe.db.escape(filters.get("sales_order"), percent=False)
	if filters.get("from_date"):
                conditions += " and so.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
		
	if filters.get("to_date"):
                conditions += " and so.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])


#       if filters.get("warehouse"):
  #             conditions += " and warehouse = '%s'" % frappe.db.escape(filters.get("warehouse"), percent=False)
        return conditions


def get_sales_order_entries(filters):
	conditions = get_conditions(filters)

	if filters.get("include_exploded_items") == "Y":
	        
        	return frappe.db.sql("""select so.name as sales_order, si.item_code as item_code, si.qty as si_qty, si.delivered_qty, bo.name, bo.company, bi.item_code as bi_item, bi.qty as bi_qty
                	from `tabSales Order` so, `tabSales Order Item` si, `tabBOM` bo, `tabBOM Explosion Item` bi where bo.name = bi.parent and so.name = si.parent and si.item_code = bo.item and so.status != "Cancelled" and si.delivered_qty < si.qty %s
                	order by so.name, si.item_code, bo.name, bi.item_code""" % conditions, as_dict=1)
	else:

        	return frappe.db.sql("""select so.name as sales_order, si.item_code as item_code, si.qty as si_qty, si.delivered_qty, bo.name, bo.company, bi.item_code as bi_item, bi.qty as bi_qty
                	from `tabSales Order` so, `tabSales Order Item` si, `tabBOM` bo, `tabBOM Item` bi where bo.name = bi.parent and so.name = si.parent and si.item_code = bo.item and so.status != "Cancelled" and si.delivered_qty < si.qty %s
       	        	order by so.name, si.item_code, bo.name, bi.item_code""" % conditions, as_dict=1)


def get_sales_order_entries_2(filters):
	conditions = get_conditions(filters)

	if filters.get("include_exploded_items") == "Y":
	        
        	return frappe.db.sql("""select so.name as sales_order, si.item_code as item_code, si.qty as si_qty, si.delivered_qty, " " as name, " " as company, " " as bi_item, 0 as bi_qty
                	from `tabSales Order` so, `tabSales Order Item` si where so.name = si.parent and so.status != "Cancelled" and si.delivered_qty < si.qty %s and not exists ( select 1 from `tabBOM` bo where bo.item = si.item_code 
                	order by so.name, si.item_code)""" % conditions, as_dict=1)

	else:

        	return frappe.db.sql("""select so.name as sales_order, si.item_code as item_code, si.qty as si_qty, si.delivered_qty, " " as name, " " as company, " " as bi_item, 0 as bi_qty
                	from `tabSales Order` so, `tabSales Order Item` si where so.name = si.parent and so.status != "Cancelled" and si.delivered_qty < si.qty %s and not exists ( select 1 from `tabBOM` bo where bo.item = si.item_code 
                	order by so.name, si.item_code)""" % conditions, as_dict=1)

def get_item_warehouse_map(filters):
        iwb_map = {}
        from_date = getdate(filters["from_date"])
        to_date = getdate(filters["to_date"])

        sle = get_sales_order_entries(filters)
	dle = get_sales_order_entries_2(filters)
#	dle = []
	company = filters.get("company")
	total_stock = 0
	if filters.get("warehouse"):
		whse = filters.get("warehouse")
	else:
		whse = get_warehouses(company)
	
	
        for d in sle:
		if filters.get("warehouse"):
			key = (d.sales_order, d.name, d.item_code, whse)
				
                	if key not in iwb_map:
                        	iwb_map[key] = frappe._dict({
                                	"opening_qty": 0.0, "opening_val": 0.0,
                                	"in_qty": 0.0, "in_val": 0.0,
                                	"out_qty": 0.0, "out_val": 0.0,
					"si_qty": 0.0,
                                	"bal_qty": 0.0, 
                                	"bi_qty": 0.0,
                                	"val_rate": 0.0, "uom": None
                        	})

	                qty_dict = iwb_map[(d.sales_order, d.name, d.item_code, whse)]
		
			qty_dict.bal_qty = get_stock(d.bi_item, whse)
		
        	        qty_dict.bi_qty = d.bi_qty
			qty_dict.si_qty = d.si_qty
			qty_dict.bi_item = d.bi_item

		else:

			total_stock = get_total_stock(d.item_code)
			if total_stock > 0:

				for w in whse:

					whse_stock = get_stock(d.item_code, w)

					if whse_stock > 0:
			                	key = (d.sales_order, d.name, d.item_code, w)
					
        		        		if key not in iwb_map:
        		                		iwb_map[key] = frappe._dict({
        		                        		"opening_qty": 0.0, "opening_val": 0.0,
        		                        		"in_qty": 0.0, "in_val": 0.0,
        		                        		"out_qty": 0.0, "out_val": 0.0,
								"si_qty": 0.0,
        		                        		"bal_qty": 0.0, 
        		                        		"bi_qty": 0.0,
        		                        		"val_rate": 0.0, "uom": None
        		                		})

			                	qty_dict = iwb_map[(d.sales_order, d.name, d.item_code, w)]
			
						qty_dict.bal_qty = whse_stock
		
        			        	qty_dict.bi_qty = d.bi_qty
						qty_dict.si_qty = d.si_qty
						qty_dict.bi_item = d.bi_item
			
			else:

				key = (d.sales_order, d.name, d.item_code, " ")
					
        	        	if key not in iwb_map:
        	                	iwb_map[key] = frappe._dict({
        	                        	"opening_qty": 0.0, "opening_val": 0.0,
        	                        	"in_qty": 0.0, "in_val": 0.0,
        	                        	"out_qty": 0.0, "out_val": 0.0,
						"si_qty": 0.0,
        	                        	"bal_qty": 0.0, 
        	                        	"bi_qty": 0.0,
        	                        	"val_rate": 0.0, "uom": None
        	                	})

		                qty_dict = iwb_map[(d.sales_order, d.name, d.item_code, " ")]
		
				qty_dict.bal_qty = 0
		
        		        qty_dict.bi_qty = d.bi_qty
				qty_dict.si_qty = d.si_qty
				qty_dict.bi_item = d.bi_item
	
	if dle:
		for d in dle:
			if filters.get("warehouse"):
				key = (d.sales_order, d.name, d.item_code, whse)
					
                		if key not in iwb_map:
                	        	iwb_map[key] = frappe._dict({
                                	"opening_qty": 0.0, "opening_val": 0.0,
                                	"in_qty": 0.0, "in_val": 0.0,
                                	"out_qty": 0.0, "out_val": 0.0,
					"si_qty": 0.0,
                                	"bal_qty": 0.0, 
                                	"bi_qty": 0.0,
                                	"val_rate": 0.0, "uom": None
                	        	})

	        	        qty_dict = iwb_map[(d.sales_order, d.name, d.item_code, whse)]
		
				qty_dict.bal_qty = get_stock(d.bi_item, whse)
			
        		        qty_dict.bi_qty = d.bi_qty
				qty_dict.si_qty = d.si_qty
				qty_dict.bi_item = d.bi_item

			else:

				total_stock = get_total_stock(d.item_code)
				if total_stock > 0:

					for w in whse:
		
						whse_stock = get_stock(d.item_code, w)

						if whse_stock > 0:
				                	key = (d.sales_order, d.name, d.item_code, w)
							
        			        		if key not in iwb_map:
        			                		iwb_map[key] = frappe._dict({
        		                        		"opening_qty": 0.0, "opening_val": 0.0,
        		                        		"in_qty": 0.0, "in_val": 0.0,
        		                        		"out_qty": 0.0, "out_val": 0.0,
								"si_qty": 0.0,
        		                        		"bal_qty": 0.0, 
        		                        		"bi_qty": 0.0,
        		                        		"val_rate": 0.0, "uom": None
        			                		})

				                	qty_dict = iwb_map[(d.sales_order, d.name, d.item_code, w)]
			
							qty_dict.bal_qty = whse_stock
		
        				        	qty_dict.bi_qty = d.bi_qty
							qty_dict.si_qty = d.si_qty
							qty_dict.bi_item = d.bi_item
			
				else:

					key = (d.sales_order, d.name, d.item_code, " ")
					
        		        	if key not in iwb_map:
        		                	iwb_map[key] = frappe._dict({
        	                        	"opening_qty": 0.0, "opening_val": 0.0,
        	                        	"in_qty": 0.0, "in_val": 0.0,
        	                        	"out_qty": 0.0, "out_val": 0.0,
						"si_qty": 0.0,
        	                        	"bal_qty": 0.0, 
        	                        	"bi_qty": 0.0,
        	                        	"val_rate": 0.0, "uom": None
        		                	})

			                qty_dict = iwb_map[(d.sales_order, d.name, d.item_code, " ")]
		
					qty_dict.bal_qty = 0
		
        			        qty_dict.bi_qty = d.bi_qty
					qty_dict.si_qty = d.si_qty
					qty_dict.bi_item = d.bi_item
				
	return iwb_map

	      
def get_warehouses(company):
		whse = frappe.db.sql("""select name from `tabWarehouse` where company = %s""", company)
		return whse

def get_stock(bi_item, warehouse):
		
	max_posting_date = frappe.db.sql("""select max(posting_date) from `tabStock Ledger Entry`
		where item_code=%s and warehouse = %s""",
		(bi_item, warehouse))[0][0]
	max_posting_date = getdate(max_posting_date)
	max_posting_date1 = datetime.datetime.strftime(max_posting_date, "%Y-%m-%d")
	
	max_posting_time = frappe.db.sql("""select max(posting_time) from `tabStock Ledger Entry`
		where item_code=%s and warehouse = %s and posting_date = %s""",
		(bi_item, warehouse, max_posting_date))[0][0]
	
#	max_posting_time = gettime(max_posting_time)
#	max_posting_time1 = datetime.datetime.strftime(max_posting_time, "%H:%M:%S")

	ssle = frappe.db.sql("""select voucher_no, voucher_type, actual_qty, qty_after_transaction
		from `tabStock Ledger Entry` sle
		where item_code=%s and warehouse = %s and posting_date = %s and posting_time = %s""",
		(bi_item, warehouse, getdate(max_posting_date1), max_posting_time))

	if ssle:

		item_stock = ssle[0][3]
	else:
		item_stock = 0
	
				
	return item_stock

def get_total_stock(item_code):
		
                item_stock = flt(frappe.db.sql("""select sum(actual_qty)
			from `tabStock Ledger Entry`
			where item_code=%s""",
			(item_code))[0][0])
		
		stock_recon = flt(frappe.db.sql("""select sum(qty_after_transaction)
			from `tabStock Ledger Entry`
			where item_code=%s and voucher_type = 'Stock Reconciliation'""",
			(item_code))[0][0])

		tot_stock = item_stock + stock_recon
		return tot_stock

def get_stock_val(item_code, warehouse):
		
                item_stock_val = flt(frappe.db.sql("""select sum(stock_value)
			from `tabStock Ledger Entry`
			where item_code=%s and warehouse = %s""",
			(item_code, warehouse))[0][0])

		stock_recon_val = flt(frappe.db.sql("""select sum(stock_value_difference)
			from `tabStock Ledger Entry`
			where item_code=%s and voucher_type = 'Stock Reconciliation'""",
			(item_code))[0][0])

		tot_stock_val = item_stock_val + stock_recon_val
		
       	        return tot_stock_val

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



