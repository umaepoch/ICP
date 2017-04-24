from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, comma_or, getdate
from frappe import _, throw, msgprint
from frappe.model.mapper import get_mapped_doc
from erpnext.hr.doctype.leave_application.leave_application \
	import get_leave_allocation_records, get_leave_balance_on, get_approved_leaves_for_period, get_number_of_leave_days


@frappe.whitelist()
def get_leave_balance_on(employee, leave_type, date, allocation_records=None,
		consider_all_leaves_in_the_allocation_period=False):
	if allocation_records == None:
		allocation_records = get_leave_allocation_records(date, employee).get(employee, frappe._dict())

	allocation = allocation_records.get(leave_type, frappe._dict())

	if consider_all_leaves_in_the_allocation_period:
		date = allocation.to_date
	leaves_taken = get_approved_leaves_for_period(employee, leave_type, allocation.from_date, date)
		
	return flt(allocation.total_leaves_allocated) - flt(leaves_taken)


@frappe.whitelist()
def get_approved_leaves_for_period(employee, leave_type, from_date, to_date):

	leave_applications = frappe.db.sql("""
		select employee, leave_type, from_date, to_date, total_leave_days
		from `tabLeave Application`
		where employee=%(employee)s and leave_type=%(leave_type)s
			and status="Approved" and docstatus=1
			and (from_date between %(from_date)s and %(to_date)s
				or to_date between %(from_date)s and %(to_date)s
				or (from_date < %(from_date)s and to_date > %(to_date)s))
	""", {
		"from_date": from_date,
		"to_date": to_date,
		"employee": employee,
		"leave_type": leave_type
	}, as_dict=1)

	leave_days = 0
	for leave_app in leave_applications:
		if leave_app.from_date >= getdate(from_date) and leave_app.to_date <= getdate(to_date):
			leave_days += leave_app.total_leave_days
		else:
			if leave_app.from_date < getdate(from_date):
				leave_app.from_date = from_date
			if leave_app.to_date > getdate(to_date):
				leave_app.to_date = to_date

			leave_days += get_number_of_leave_days(employee, leave_type,
				leave_app.from_date, leave_app.to_date)

	return leave_days


