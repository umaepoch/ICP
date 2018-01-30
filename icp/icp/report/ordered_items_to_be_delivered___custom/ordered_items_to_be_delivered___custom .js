{
 "add_total_row": 1, 
 "apply_user_permissions": 1, 
 "creation": "2018-01-10 15:42:20.976835", 
 "disabled": 0, 
 "docstatus": 0, 
 "doctype": "Report", 
 "idx": 0, 
 "is_standard": "Yes", 
 "letter_head": "GST Letterhead Unit2", 
 "modified": "2018-01-11 09:26:34.907682", 
 "modified_by": "Administrator", 
 "module": "Icp", 
 "name": "Ordered Items To Be Delivered - Custom", 
 "owner": "Administrator", 
 "query": "select \n `tabSales Order`.`assigned_to` as \"Assigned To::120\",\n `tabSales Order`.`name` as \"Sales Order:Link/Sales Order:120\",\n `tabSales Order`.`customer` as \"Customer:Link/Customer:120\",\n `tabSales Order`.`customer_name` as \"Customer Name::150\",\n `tabSales Order`.`transaction_date` as \"Date:Date\",\n `tabSales Order`.`project` as \"Project:Link/Project:120\",\n `tabSales Order Item`.item_code as \"Item:Link/Item:120\",\n `tabSales Order Item`.description as \"Description::200\",\n `tabSales Order Item`.qty as \"Qty:Float:140\",\n `tabSales Order Item`.delivered_qty as \"Delivered Qty:Float:140\",\n (`tabSales Order Item`.qty - ifnull(`tabSales Order Item`.delivered_qty, 0)) as \"Qty to Deliver:Float:140\",\n `tabSales Order Item`.base_rate as \"Rate:Float:140\",\n `tabSales Order Item`.base_amount as \"Amount:Float:140\",\n ((`tabSales Order Item`.qty - ifnull(`tabSales Order Item`.delivered_qty, 0))*`tabSales Order Item`.base_rate) as \"Amount to Deliver:Float:140\",\n `tabBin`.actual_qty as \"Available Qty:Float:120\",\n `tabBin`.projected_qty as \"Projected Qty:Float:120\",\n `tabSales Order Item`.`delivery_date` as \"Item Delivery Date:Date:120\",\nDATEDIFF(Curdate(), `tabSales Order Item`.`delivery_date`) as \"Delay Days:Int:140\",\n `tabSales Order Item`.item_name as \"Item Name::150\",\n `tabSales Order Item`.item_group as \"Item Group:Link/Item Group:120\",\n `tabSales Order Item`.warehouse as \"Warehouse:Link/Warehouse:200\"\nfrom\n `tabSales Order` JOIN `tabSales Order Item` \n LEFT JOIN `tabBin` ON (`tabBin`.item_code = `tabSales Order Item`.item_code\n and `tabBin`.warehouse = `tabSales Order Item`.warehouse)\nwhere\n `tabSales Order Item`.`parent` = `tabSales Order`.`name`\n and `tabSales Order`.docstatus = 1\n and `tabSales Order`.status not in (\"Stopped\", \"Closed\")\n and ifnull(`tabSales Order Item`.delivered_qty,0) < ifnull(`tabSales Order Item`.qty,0)\norder by `tabSales Order`.transaction_date asc", 
 "ref_doctype": "Delivery Note", 
 "report_name": "Ordered Items To Be Delivered - Custom", 
 "report_type": "Query Report", 
 "roles": [
  {
   "role": "Stock User"
  }, 
  {
   "role": "Stock Manager"
  }, 
  {
   "role": "Sales User"
  }, 
  {
   "role": "Accounts User"
  }
 ]
}