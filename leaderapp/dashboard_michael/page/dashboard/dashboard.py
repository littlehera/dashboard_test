# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function
import frappe
from frappe.utils import add_to_date
import datetime

@frappe.whitelist()
def get_dashboard(doctype, timespan, company, field):
    """return top 10 items for that doctype based on conditions"""
    from_date = get_from_date(timespan)
    records = []
    if doctype == "Customer":
        records = get_all_customers(from_date, company, field)
    elif doctype == "Sales Order":
        records = get_all_salesorder_customer(from_date, company, field)

    return records

@frappe.whitelist()
def get_dashboard0(doctype, timespan, company, field):
    """return top 10 items for that doctype based on conditions"""
    from_date = get_from_date(timespan)
    records = []
    if doctype == "Customer":
        records = get_all_customers(from_date, company, field)
    elif doctype == "Sales Order":
        records = get_all_items(from_date, company, field)

    return records

@frappe.whitelist()
def get_dashboard1(doctype, timespan, company, field):
    """return top 10 items for that doctype based on conditions"""
    from_date = get_from_date(timespan)
    records = []
    if doctype == "Customer":
        records = get_all_customers(from_date, company, field)
    elif doctype == "Sales Order":
        records = get_all_salesorder(from_date, company, field)

    return records


@frappe.whitelist()
def get_dashboard2(doctype, timespan, company, field):
    """return top 10 items for that doctype based on conditions"""
    from_date = get_from_date(timespan)
    records = []
    if doctype == "Customer":
        records = get_all_customers(from_date, company, field)
    elif doctype == "Sales Order":
        records = get_all_salesorder_delivery(from_date, company, field)

    return records

@frappe.whitelist()
def get_dashboard3(doctype, timespan, company, field):
    """return top 10 items for that doctype based on conditions"""
    from_date = get_from_date(timespan)
    records = []
    if doctype == "Customer":
        records = get_all_customers(from_date, company, field)
    elif doctype == "Sales Order":
        records = get_all_salesorder_customer(from_date, company, field)

    return records


@frappe.whitelist()
def get_dashboard4(doctype, timespan, company, field):
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
			select transaction_date as name, sum(grand_total) as value
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
    now = datetime.datetime.now();
    print(now.strftime("%Y-%m-%d"))
    if field == "grand_total":
        return frappe.db.sql("""
			select transaction_date as name, sum(grand_total) as value
			FROM `tabSales Order`
			where docstatus = 1 and transaction_date >= %s and company = %s
			group by transaction_date
			order by transaction_date ASC
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

def get_all_salesorder_delivery(from_date, company, field):
    if field == "grand_total":
        return frappe.db.sql("""
			select delivery_date as name, sum(grand_total) as value
			FROM `tabSales Order`
			where docstatus = 1 and transaction_date >= %s and company = %s
			group by delivery_date
			order by delivery_date ASC
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

def get_all_salesorder_customer(from_date, company, field):
    print("===================================================================")
    print("===================================================================")
    print((datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d'))
    print((datetime.datetime.now() - datetime.timedelta(7)).strftime('%Y-%m-%d'))
    print("===================================================================")
    print("===================================================================")

    yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')

    if field == "grand_total":
        return frappe.db.sql("""
			select %s as name, sum(grand_total) as value
			FROM `tabSales Order`
			where docstatus = 1 and status = "To Deliver and Bill" and transaction_date = %s and company = %s
			group by transaction_date
			order by value DESC
			limit 20
		""", (yesterday, yesterday, company), as_dict=1)
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

def get_all_items(from_date, company, field):
	if field == "grand_total":
		return frappe.db.sql("""
			select item_code as name, {0} as value
			from tabBin
			group by item_code
			order by value desc
			limit 20
		""".format("sum(actual_qty)" if field=="available_stock_qty" else "sum(stock_value)"), as_dict=1)
	else:
		if field == "base_grand_total":
			select_field = "sum(order_item.base_net_amount)"
			select_doctype = "Sales Order"
		elif field == "total_purchase_amount":
			select_field = "sum(order_item.base_net_amount)"
			select_doctype = "Purchase Order"
		# elif field == "total_qty_sold":
		# 	select_field = "sum(order_item.stock_qty)"
		# 	select_doctype = "Sales Order"
		# elif field == "total_qty_purchased":
		# 	select_field = "sum(order_item.stock_qty)"
		# 	select_doctype = "Purchase Order"

		return frappe.db.sql("""
			select order_item.item_code as name, {0} as value
			from `tab{1}` sales_order join `tab{1} Item` as order_item
				on sales_order.name = order_item.parent
			where sales_order.docstatus = 1
				and sales_order.company = %s and sales_order.transaction_date >= %s
			group by order_item.item_code
			order by value desc
			limit 20
		""".format(select_field, select_doctype), (company, from_date), as_dict=1)

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