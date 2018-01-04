# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, utils
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
        order_prev = ""
	cust_prev = ""
	pono_prev = ""
	sodate_prev = ""
        order_work = "" 
        item_prev = ""
        item_work = ""
	desc_prev = ""
	desc_work = ""
	deldate_prev = ""
	diff_days_prev = ""
	custgroup_prev = ""
	itemgroup_prev = ""
	so_ass_prev = ""
	status_prev = ""
        order_count = 0 
	item_count = 0
        tot_bal_qty = 0 
	tot_si_qty = 0
	tot_del_qty = 0
	tot_pend_qty = 0
	tot_pend_val = 0
	item_pend_qty = 0
	item_pend_rate = 0
	item_pend_val = 0
	item_del_qty = 0
	temp_date = getdate("2001-01-01")
	curr_date = utils.today()
	diff_days = 0
	per_qty = 0
	full_tot_del_amt = 0
	full_tot_si_amt = 0
	tot_per_amt = 0
	tot_del_qty = 0
	tot_si_qty = 0
	full_tot_del_qty = 0
	full_tot_si_qty = 0
	tot_del_on_time = 0
	tot_per_qty = 0
	full_tot_per_qty = 0
	

        for (sales_order, item, description, delivery_date, del_note) in sorted(iwb_map):
                qty_dict = iwb_map[(sales_order, item, description, delivery_date, del_note)]
                data.append([
                        sales_order, qty_dict.so_date, qty_dict.so_del_date, delivery_date, qty_dict.customer, item, 
			item_map[item]["item_group"], item_map[item]["description"], item_map[item]["brand"],                    
                        qty_dict.si_qty, del_note, qty_dict.del_qty, qty_dict.pend_qty, qty_dict.customer_group, qty_dict.assigned_to, 				qty_dict.amount, qty_dict.total, qty_dict.status, qty_dict.po_no, qty_dict.pend_val, qty_dict.rate
                        
                    ])

	for rows in data: 
       		if order_count == 0: 
       			order_prev = rows[0] 
 			item_prev = rows[5]
			cust_prev = rows[4]
			pono_prev = rows[18]
			sodate_prev = rows[1]
			desc_prev = rows[7]
			deldate_prev = rows[2]
			custgroup_prev = rows[13]
			itemgroup_prev = rows[6]
			so_ass_prev = rows[14]
			status_prev = rows[17]
			tot_si_qty = tot_si_qty + rows[9]


			full_tot_si_amt = full_tot_si_amt + rows[15]
			full_tot_si_qty = full_tot_si_qty + rows[9]
                        tot_del_qty = tot_del_qty + rows[11] 
			
			item_pend_qty = rows[9] - rows[11]
			tot_pend_qty = tot_pend_qty + item_pend_qty
			item_pend_val = rows[19]
			item_pend_rate = rows[20]
			item_del_qty = rows[11]
						
			if rows[3] == temp_date:
				diff_days = getdate(curr_date) - rows[2]
			else:
				diff_days = rows[3] - rows[2]
			
			if rows[3] <= rows[2] and rows[3] != temp_date:
				full_tot_del_amt = full_tot_del_amt + rows[16]
				full_tot_del_qty = full_tot_del_qty + rows[11]
				tot_del_on_time = tot_del_on_time + rows[11]
				per_qty = (item_del_qty / tot_si_qty) * 100

			if rows[3] == temp_date:
				rows[3] = " "
			diff_days_prev = diff_days
			summ_data.append([order_prev, rows[4], rows[18], rows[1],
			 	rows[5], rows[7], rows[2], " ", " ", " ", " ", rows[9],
				 rows[11], per_qty, rows[13], rows[6], rows[14], rows[17], rows[10], rows[3], rows[16]
 				]) 
                else: 

						
			order_work = rows[0]
                        item_work = rows[5]
			desc_work = rows[7]
			if rows[3] == temp_date:
				diff_days = getdate(curr_date) - rows[2]

			else:
				diff_days = rows[3] - rows[2]
			
				
			if order_prev == order_work: 
				tot_del_qty = tot_del_qty + rows[11]
												
							
                                if desc_prev == desc_work:
					item_del_qty = item_del_qty + rows[11]
					item_pend_qty = rows[9] - item_del_qty
					item_pend_val = rows[19]
					item_pend_rate = rows[20]
								
				else:
					diff_days_temp = getdate(curr_date) - deldate_prev
					if status_prev == "To Deliver and Bill":
						if item_pend_qty > 0:				
	
							summ_data.append([order_prev, cust_prev, pono_prev, sodate_prev, item_prev, desc_prev, deldate_prev, item_pend_qty, item_pend_rate, item_pend_val, diff_days_temp, " ", " ", " ", custgroup_prev, itemgroup_prev, so_ass_prev, status_prev ," ", " ", " "	
 						])
					else:
						summ_data.append([order_prev, cust_prev, pono_prev, sodate_prev, item_prev, desc_prev, deldate_prev, item_pend_qty, item_pend_rate, item_pend_val, diff_days_temp, " ", " ", " ", custgroup_prev, itemgroup_prev, so_ass_prev, status_prev ," ", " ", " "	
 						])

					if item_prev != item_work:
						item_prev = item_work

					desc_prev = desc_work
					cust_prev = rows[4]
					pono_prev = rows[18]
					sodate_prev = rows[1]
					deldate_prev = rows[2]
					diff_days_prev = diff_days
					custgroup_prev = rows[13]
					itemgroup_prev = rows[6]
					so_ass_prev = rows[14]
					status_prev = rows[17]
					item_del_qty = rows[11]
					item_pend_qty = 0
					item_pend_rate = 0
					item_pend_val = 0
					per_qty = 0
					tot_si_qty = tot_si_qty + rows[9]
					full_tot_si_amt = full_tot_si_amt + rows[15]
					full_tot_si_qty = full_tot_si_qty + rows[9]	
					item_pend_qty = rows[9] - item_del_qty
					tot_pend_qty = tot_pend_qty + item_pend_qty

					item_pend_val = rows[19]
					item_pend_rate = rows[20]
				
				differ_days = diff_days
		#		
				if rows[3] <= rows[2] and rows[3] != temp_date:
					full_tot_del_amt = full_tot_del_amt + rows[16]
					full_tot_del_qty = full_tot_del_qty + rows[11]
					tot_del_on_time = tot_del_on_time + rows[11]
										
					per_qty = (item_del_qty / rows[9]) * 100
	
				if rows[3] == temp_date:
					rows[3] = " "
				if status_prev == "To Deliver and Bill":
					if item_pend_qty > 0:
						summ_data.append([order_prev, rows[4], rows[18], rows[1],
			 			rows[5], rows[7], rows[2], " ", " ", " ", " ", rows[9],
						 rows[11], per_qty, rows[13], rows[6], rows[14], rows[17], rows[10], rows[3], rows[16] 
 						]) 
				else:
					summ_data.append([order_prev, rows[4], rows[18], rows[1],
			 			rows[5], rows[7], rows[2], " ", " ", " ", " ", rows[9],
						 rows[11], per_qty, rows[13], rows[6], rows[14], rows[17], rows[10], rows[3], rows[16] 
 						]) 
			else: 
				diff_days_temp = getdate(curr_date) - deldate_prev
				if status_prev == "To Deliver and Bill":
					if item_pend_qty > 0:		
						summ_data.append([order_prev, cust_prev, pono_prev, sodate_prev,
					 	item_prev, desc_prev, deldate_prev, item_pend_qty, item_pend_rate, item_pend_val, diff_days_temp, " ", " ", " ", custgroup_prev, itemgroup_prev, so_ass_prev, status_prev," ", " ",  " "
	 				]) 
				else:
					summ_data.append([order_prev, cust_prev, pono_prev, sodate_prev,
					 	item_prev, desc_prev, deldate_prev, item_pend_qty, item_pend_rate, item_pend_val, diff_days_temp, " ", " ", " ", custgroup_prev, itemgroup_prev, so_ass_prev, status_prev," ", " ",  " "
	 				]) 
				if rows[17] == 'Closed' or rows[17] == 'Completed':
					if tot_del_qty > 0:
						tot_per_qty = (tot_del_on_time / tot_del_qty) * 100
					else:
						tot_per_qty = 0
				else:
					if tot_si_qty > 0:
						tot_per_qty = (tot_del_on_time / tot_si_qty) * 100
					else:
						tot_per_qty = 0

				#summ_data.append([" ", " ", " ", order_prev, " ", 
#			 	" ", " ", " ", " ", tot_si_qty, tot_del_qty, " ", tot_per_qty, tot_pend_qty, " ", " ",  " "   
#				
 #				])	
				item_pend_qty = 0
				item_pend_rate = 0
				item_pend_val = 0
				tot_si_qty = 0
				tot_del_qty = 0

				tot_del_on_time = 0
				per_qty = 0
                                tot_si_qty = tot_si_qty + rows[9]
				full_tot_si_amt = full_tot_si_amt + rows[15]
				full_tot_si_qty = full_tot_si_qty + rows[9]
                        	tot_del_qty = tot_del_qty + rows[11] 
				full_tot_del_qty = full_tot_del_qty + rows[11]

				item_del_qty = rows[11]		 	 
				item_pend_qty = rows[9] - rows[11] - item_pend_qty
				tot_pend_qty = tot_pend_qty + item_pend_qty

				item_pend_val = rows[19] - item_pend_val
				item_pend_rate = rows[20]

				differ_days = flt(diff_days)

				if rows[3] <= rows[2] and rows[3] != temp_date:
					full_tot_del_amt = full_tot_del_amt + rows[16]
					full_tot_del_qty = full_tot_del_qty + rows[11]
					tot_del_on_time = tot_del_on_time + rows[11]
					per_qty = (item_del_qty / tot_si_qty) * 100
		
				if rows[3] == temp_date:
					rows[3] = " "
				if status_prev == "To Deliver and Bill":
					if item_pend_qty >0:
						summ_data.append([order_work, rows[4], rows[18], rows[1],
					 	rows[5], rows[7], rows[2], " "," ", " ", " ", rows[9],
						 rows[11], per_qty, rows[13], rows[6], rows[14], rows[17], rows[10], rows[3], rows[16]
 						]) 
				else:
                                	summ_data.append([order_work, rows[4], rows[18], rows[1],
					 	rows[5], rows[7], rows[2], " "," ", " ", " ", rows[9],
						 rows[11], per_qty, rows[13], rows[6], rows[14], rows[17], rows[10], rows[3], rows[16]
 						]) 
				
				order_prev = order_work 
                                item_prev = item_work
				desc_prev = desc_work
				cust_prev = rows[4]
				pono_prev = rows[18]
				sodate_prev = rows[1]
				desc_prev = rows[7]
				deldate_prev = rows[2]
				diff_days_prev = diff_days
				custgroup_prev = rows[13]
				itemgroup_prev = rows[6]
				so_ass_prev = rows[14]
				status_prev = rows[17]

									
		order_count = order_count + 1 
	if full_tot_si_amt > 0:

		tot_per_amt = (full_tot_del_amt / full_tot_si_amt) * 100
		tot_per_qty = (full_tot_del_qty / full_tot_si_qty) * 100
	else:
		tot_per_amt = 0
		tot_per_qty = 0

#	summ_data.append([" ", " ", " ", order_prev, " ", 
#			 	" ", " ", " ", " ", tot_si_qty, tot_del_qty, " ", per_qty, tot_pend_qty, " ", " ",  " " 
 #				])		 
	summ_data.append([order_prev, cust_prev, pono_prev, sodate_prev,
					 	item_prev, desc_prev, deldate_prev, item_pend_qty, item_pend_rate, item_pend_val, diff_days_prev, " ", " ", per_qty, custgroup_prev, itemgroup_prev, so_ass_prev, status_prev," ", " ", " " ]) 

	summ_data.append([" ", " ", " ", " ", " ", " ",
			 	" ",  tot_pend_qty, 0, 0, " ", full_tot_si_qty, full_tot_del_qty, per_qty, " ", " ",  " ", " ", " ", " ", " "
 				])		 

	summ_data.append([" ", " ", " ", " ", " ", "Total Value and Percentage ", " ",
			 	" ", " ", full_tot_si_amt, 0, full_tot_del_amt, tot_per_amt, tot_per_qty, " ", " ",  " ", " ", " ", " "
 				])
		 
		 						 
	return columns, summ_data 


def get_columns():
        """return columns"""
               
        columns = [
		
		_("Sales Order")+":Link/Sales Order:120",
		_("SO Customer")+"::80",
		_("Customer PO No")+"::80",
		_("SO Date")+":Date:75",
		_("Item")+":Link/Item:100",
		_("Description")+":Text Editor:120",
		_("SO Delivery Date")+":Date:75",
		_("SO Bal Qty")+":Int:70",
		_("SO Rate")+":Int:70",
		_("SO Bal Value")+":Int:70",
		_("Delay by")+":Int:50",
		_("SO Qty")+":Int:70",
		_("DN Qty")+":Int:70",
		_("% On Time Delivery")+":Int:70",
		_("Cust Group")+"::80",
		_("Item Group")+"::100",
		_("SO Assigned")+"::80",
		_("SO Status")+"::80",
		_("Delivery Note")+":Link/Delivery Note:100",
		_("DN Date")+":Date:80",
		_("DN Amount")+":Int:80"

       	        		
		 
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

	if filters.get("so_status"):
		so_status = filters.get("so_status")
		if so_status != "All":
	                conditions += " and so.status = '%s'" % frappe.db.escape(filters.get("so_status"), percent=False)

	if filters.get("doc_status"):
                conditions += " and so.docstatus = '%s'" % frappe.db.escape(filters.get("doc_status"), percent=False)
	
	if filters.get("item_group"):
                conditions += " and si.item_group = '%s'" % frappe.db.escape(filters.get("item_group"), percent=False)
	
	if filters.get("cust_group"):
                conditions += " and so.customer_group = '%s'" % frappe.db.escape(filters.get("cust_group"), percent=False)

        if filters.get("customer"):
                conditions += " and so.customer = '%s'" % frappe.db.escape(filters.get("customer"), percent=False)

	return conditions

def get_sales_details_w_dn(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select so.name as sales_order, so.po_no, so._assign, so.transaction_date as date, so.customer, so.customer_group as customer_group, so.delivery_date as sodel_date, so.status, si.item_code, si.idx as si_idx, si.description, si.warehouse, si.qty as si_qty, si.delivered_qty as delivered_qty, si.rate as item_rate, si.amount, si.billed_amt, dni.qty as del_qty, dn.posting_date as delivery_date, dni.amount as total, dni.parent as del_note
                from `tabDelivery Note Item` dni, `tabDelivery Note` dn, `tabSales Order Item` si, `tabSales Order` so
                where dni.item_code = si.item_code and dn.status in ("Completed", "To Bill") and so.name = si.parent and dn.name = dni.parent and dni.against_sales_order = so.name and si.item_group != "Consumable" and si.item_group != "Raw Material" %s order by so.name, si.item_code, dn.posting_date asc, si.warehouse""" % conditions, as_dict=1)

def get_sales_details_w_inv(filters):
        conditions = get_conditions(filters)
	
        return frappe.db.sql("""select so.name as sales_order, so.po_no, so._assign, so.transaction_date as date, so.customer, so.customer_group as customer_group, so.delivery_date as sodel_date, so.status, si.item_code, si.idx as si_idx, si.description, si.warehouse, si.qty as si_qty, si.delivered_qty as delivered_qty, si.rate as item_rate, si.amount, si.billed_amt, sli.qty as del_qty, sl.posting_date as delivery_date, sli.amount as total, sli.parent as del_note
                from `tabSales Invoice Item` sli, `tabSales Invoice` sl, `tabSales Order Item` si, `tabSales Order` so
                where sli.item_code = si.item_code and so.name = si.parent and sl.name = sli.parent and sli.sales_order = so.name and si.item_group != "Consumable" and si.item_group != "Raw Material" and sl.update_stock = 1 and sl.status != "Cancelled" %s and not exists (
                select 1 from `tabDelivery Note Item` dni where dni.against_sales_order = so.name) order by so.name, si.item_code, sl.posting_date asc, si.warehouse""" % conditions, as_dict=1)



def get_sales_details_wo_dn_inv(filters):
        conditions = get_conditions(filters)

#	if not (conditions):	
	return frappe.db.sql("""select so.name as sales_order, so.po_no, so._assign, so.transaction_date as date, so.customer, so.customer_group as customer_group, so.delivery_date as sodel_date, so.status, si.item_code, si.idx as si_idx, si.description, si.warehouse, si.qty as si_qty, si.delivered_qty as delivered_qty, si.rate as item_rate, si.amount, si.billed_amt, 0 as del_qty, date("2001-01-01") as delivery_date, 0 as total, " " as del_note
                from `tabSales Order Item` si, `tabSales Order` so where so.name = si.parent %s and si.item_group != "Consumable" and si.item_group != "Raw Material" and not exists (
                select 1 from `tabDelivery Note Item` dni where dni.against_sales_order = so.name and dni.item_code = si.item_code) and not exists (
                select 1 from `tabSales Invoice Item` sli where sli.sales_order = so.name and sli.item_code = si.item_code) order by so.name, si.item_code""" % conditions, as_dict=1)
#	else:
#		return

def get_item_map(filters):
        iwb_map = {}
#        from_date = getdate(filters["from_date"])
 #       to_date = getdate(filters["to_date"])
	
        sle = get_sales_details_w_dn(filters)
        
	dle = get_sales_details_w_inv(filters)

	kle = get_sales_details_wo_dn_inv(filters)
        for d in sle:
                
                key = (d.sales_order, d.item_code, d.description, d.delivery_date, d.del_note)

                if key not in iwb_map:
                	iwb_map[key] = frappe._dict({
                                "si_qty": 0.0, "del_qty": 0.0,
				"pend_qty": 0.0, "amount": 0.0,
				"total": 0.0,
                                "val_rate": 0.0, "uom": None
                        })

                qty_dict = iwb_map[(d.sales_order, d.item_code, d.description, d.delivery_date, d.del_note)]

                
                qty_dict.si_qty = d.si_qty
                qty_dict.del_qty = d.del_qty
                qty_dict.delivered_qty = d.delivered_qty
                qty_dict.so_date = d.date
		temp_date = getdate("2001-01-01")
		if d.sodel_date == " ":
			qty_dict.so_del_date = temp_date
		else:
			qty_dict.so_del_date = d.sodel_date
        #        qty_dict.del_date = d.delivery_date
                qty_dict.customer = d.customer
		qty_dict.assigned_to = d._assign
		qty_dict.status = d.status
		qty_dict.po_no = d.po_no
		qty_dict.customer_group = d.customer_group
#		qty_dict.description = d.description
		qty_dict.rate = d.item_rate
		qty_dict.amount = d.amount
		qty_dict.billed_amt = d.billed_amt
		qty_dict.total = d.total
		qty_dict.pend_val = qty_dict.amount - qty_dict.billed_amt
                if qty_dict.si_qty > qty_dict.del_qty:
              		qty_dict.pend_qty = qty_dict.si_qty - qty_dict.del_qty - qty_dict.delivered_qty
			
	if dle:
		for d in dle:

        	        key = (d.sales_order, d.item_code, d.description, d.delivery_date, d.del_note)
        	        if key not in iwb_map:
        	                iwb_map[key] = frappe._dict({
        	                        "si_qty": 0.0, "del_qty": 0.0,
					"pend_qty": 0.0, "amount": 0.0,
					"total": 0.0,
        	                        "val_rate": 0.0, "uom": None
        	                })

        	        qty_dict = iwb_map[(d.sales_order, d.item_code, d.description, d.delivery_date, d.del_note)]

                
        	        qty_dict.si_qty = d.si_qty
        	        qty_dict.del_qty = d.del_qty
        	        qty_dict.delivered_qty = d.delivered_qty
        	        qty_dict.so_date = d.date
			temp_date = getdate("2001-01-01")
			
			if d.sodel_date == " ":
				qty_dict.so_del_date = temp_date
			
			else:
				qty_dict.so_del_date = d.sodel_date

			qty_dict.so_del_date = d.sodel_date
        	#        qty_dict.del_date = d.delivery_date
        	        qty_dict.customer = d.customer
			qty_dict.assigned_to = d._assign
			qty_dict.status = d.status
			qty_dict.po_no = d.po_no
#			qty_dict.description = d.description
			qty_dict.rate = d.item_rate
			qty_dict.customer_group = d.customer_group
			qty_dict.amount = d.amount
			qty_dict.billed_amt = d.billed_amt
			qty_dict.total = d.total
			qty_dict.pend_val = qty_dict.amount - qty_dict.billed_amt
	                if qty_dict.si_qty > qty_dict.del_qty:
        	      		qty_dict.pend_qty = qty_dict.si_qty - qty_dict.del_qty - qty_dict.delivered_qty

				
	
	if kle:
		for d in kle:

        	        key = (d.sales_order, d.item_code, d.description, d.delivery_date, d.del_note)
        	        if key not in iwb_map:
        	                iwb_map[key] = frappe._dict({
        	                        "si_qty": 0.0, "del_qty": 0.0,
					"pend_qty": 0.0, "amount": 0.0,
					"total": 0.0,
        	                        "val_rate": 0.0, "uom": None
        	                })

        	        qty_dict = iwb_map[(d.sales_order, d.item_code, d.description, d.delivery_date, d.del_note)]

                
        	        qty_dict.si_qty = d.si_qty
        	        qty_dict.del_qty = d.del_qty
        	        qty_dict.delivered_qty = d.delivered_qty
        	        qty_dict.so_date = d.date
			temp_date = getdate("2001-01-01")
			
			if d.sodel_date == " ":
				qty_dict.so_del_date = temp_date
			
			else:
				qty_dict.so_del_date = d.sodel_date

			qty_dict.so_del_date = d.sodel_date
        	#        qty_dict.del_date = d.delivery_date
        	        qty_dict.customer = d.customer
			qty_dict.assigned_to = d._assign
			qty_dict.status = d.status
			qty_dict.po_no = d.po_no
#			qty_dict.description = d.description
			qty_dict.rate = d.item_rate
			qty_dict.customer_group = d.customer_group
			qty_dict.amount = d.amount
			qty_dict.billed_amt = d.billed_amt
			qty_dict.total = d.total
			qty_dict.pend_val = qty_dict.amount - qty_dict.billed_amt
        	        if qty_dict.si_qty > qty_dict.del_qty:
        	      		qty_dict.pend_qty = qty_dict.si_qty - qty_dict.del_qty - qty_dict.delivered_qty

	

               
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



