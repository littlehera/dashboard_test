# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function
import frappe
from frappe.utils import add_to_date

@frappe.whitelist()
def get_dashboard(doctype, timespan, company, field):
    """return top 10 items for that doctype based on conditions"""
    from_date = get_from_date(timespan)
    records = []
    if doctype == "Customer":
        records = get_all_customers(from_date, company, field)
    elif doctype == "Sales Order":
        records = get_all_salesorder(from_date, company, field)

    return records

def get_all_customers(from_date, company, field):
    if field == "grand_total":
        return frappe.db.sql("""
			select customer as name, sum(grand_total) as value
			FROM `tabSales Order`
			where docstatus = 1 and transaction_date >= %s and company = %s
			group by customer
			order by value DESC
			limit 20
		""", (from_date, company), as_dict=1)
    else:
        if field == "base_grand_total":
            select_field = "sum(so_item.base_net_amount)"
        elif field == "total_qty_sold":
            select_field = "sum(so_item.stock_qty)"

        return frappe.db.sql("""
			select so.customer as name, {0} as value
			FROM `tabSales Order` as so JOIN `tabSales Order Item` as so_item
				ON so.name = so_item.parent
			where so.docstatus = 1 and so.transaction_date >= %s and so.company = %s
			group by so.customer
			order by value DESC
			limit 20
		""".format(select_field), (from_date, company), as_dict=1)

def get_all_salesorder(from_date, company, field):
    if field == "grand_total":
        return frappe.db.sql("""
			select customer as name, sum(grand_total) as value
			FROM `tabSales Order`
			where docstatus = 1 and transaction_date >= %s and company = %s
			group by customer
			order by value DESC
			limit 20
		""", (from_date, company), as_dict=1)
    else:
        if field == "base_grand_total":
            select_field = "sum(so_item.base_net_amount)"
        elif field == "total_qty_sold":
            select_field = "sum(so_item.stock_qty)"

        return frappe.db.sql("""
			select so.customer as name, {0} as value
			FROM `tabSales Order` as so JOIN `tabSales Order Item` as so_item
				ON so.name = so_item.parent
			where so.docstatus = 1 and so.transaction_date >= %s and so.company = %s
			group by so.customer
			order by value DESC
			limit 20
		""".format(select_field), (from_date, company), as_dict=1)


def get_from_date(seleted_timespan):
    """return string for ex:this week as date:string"""
    days = months = years = 0
    if "month" == seleted_timespan.lower():
        months = -1
    elif "quarter" == seleted_timespan.lower():
        months = -3
    elif "year" == seleted_timespan.lower():
        years = -1
    else:
        days = -7

    return add_to_date(None, years=years, months=months, days=days,
                       as_string=True, as_datetime=True)