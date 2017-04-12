# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	salary_struc = get_salary_struc(filters)
	columns, earning_types, ded_types = get_columns(salary_struc)
	ss_earning_map = get_ss_earning_map(salary_struc)
	ss_ded_map = get_ss_ded_map(salary_struc)


	data = []
	for ss in salary_struc:
		row = [ss.employee, ss.employee_name, ss.date_of_joining, ss.designation,
			ss.status, ss.employment_type, ss.sal_struc]

		for e in earning_types:
			row.append(ss_earning_map.get(ss.name, {}).get(e))

		row += [ss.gross_pay]

		for d in ded_types:
			row.append(ss_ded_map.get(ss.name, {}).get(d))

		row += [ss.total_deduction, ss.net_pay]

		data.append(row)

	return columns, data

def get_columns(salary_struc):
	columns = [
		_("Employee") + ":Link/Employee:120", _("Employee Name") + "::140", _("Date of Joining") + "::140",  _("Designation") + ":Link/Designation:120",  _("Status") + "::120",  _("Employment Type") + "::120",  _("Salary Structure") + ":Link/Salary Structure:120",
		
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_struc))), tuple([d.name for d in salary_struc]), as_dict=1):
		salary_components[_(component.type)].append(component.salary_component)

	columns = columns + [(e + ":Currency:120") for e in salary_components[_("Earning")]] + \
		[_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120"]

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_struc(filters):
#	filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
#	conditions, filters = get_conditions(filters)
	salary_struc = frappe.db.sql("""select  emp.employee as employee, emp.employee_name, emp.date_of_joining, emp.designation, emp.status as status, emp.employment_type, sal.name as sal_struc, sal.total_earning, sal.total_deduction, sal.net_pay from `tabEmployee` emp, `tabSalary Structure` sal where emp.employee = sal.employee 
		order by employee""", as_dict=1)

	if not salary_struc:
		frappe.throw(_("No salary structure found"))
	return salary_struc


#def get_conditions(filters):
#	conditions = ""
#	if filters.get("date_range"): conditions += " and start_date >= %(from_date)s"
#	if filters.get("date_range"): conditions += " and end_date <= %(to_date)s"
#	if filters.get("company"): conditions += " and company = %(company)s"
#	if filters.get("employee"): conditions += " and employee = %(employee)s"

#	return conditions, filters

def get_ss_earning_map(salary_struc):
	ss_earnings = frappe.db.sql("""select parent, salary_component, amount
		from `tabSalary Detail` where parent in (%s)""" %
		(', '.join(['%s']*len(salary_struc))), tuple([d.name for d in salary_struc]), as_dict=1)

	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_earning_map

def get_ss_ded_map(salary_struc):
	ss_deductions = frappe.db.sql("""select parent, salary_component, amount
		from `tabSalary Detail` where parent in (%s)""" %
		(', '.join(['%s']*len(salary_struc))), tuple([d.name for d in salary_struc]), as_dict=1)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_ded_map
