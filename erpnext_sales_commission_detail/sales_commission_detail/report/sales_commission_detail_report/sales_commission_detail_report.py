# Copyright (c) 2013, Dirk van der Laarse and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()

	data = get_invoice_items(filters)

	return columns, data

def get_columns():
	"""return columns"""
	columns = [{
	    "fieldname": "posting_date",
	    "label": _("Date"),
	    "fieldtype": "Date",
	    "options": "",
	    "width": 100
	},
	{
	    "fieldname": "customer_name",
	    "label": _("Customer"),
	    "fieldtype": "Link",
	    "options": "Customer",
	    "width": 200
	},
	{
	    "fieldname": "name",
	    "label": _("Invoice"),
	    "fieldtype": "Link",
	    "options": "Sales Invoice",
	    "width": 130
	},
	{
	    "fieldname": "item_code",
	    "label": _("Item"),
	    "fieldtype": "Link",
	    "options": "Item",
	    "width": 200
	},
	{
	    "fieldname": "item_name",
	    "label": _("Item Name"),
	    "fieldtype": "",
	    "options": "",
	    "width": 100
	},
	{
	    "fieldname": "qty",
	    "label": _("Qty"),
	    "fieldtype": "",
	    "options": "",
	    "width": 30
	},
	{
	    "fieldname": "rate",
	    "label": _("Rate"),
	    "fieldtype": "Currency",
	    "options": "currency",
	    "width": 60
	},
	{
	    "fieldname": "total",
	    "label": _("Total"),
	    "fieldtype": "Currency",
	    "options": "currency",
	    "width": 60
	},
	{
	    "fieldname": "commission_rate",
	    "label": _("Commission Rate"),
	    "fieldtype": "",
	    "options": "",
	    "width": 60
	},
	{
	    "fieldname": "total_commission",
	    "label": _("Total Commission"),
	    "fieldtype": "Currency",
	    "options": "currency",
	    "width": 60
	}]

	return columns

def get_invoice_items(filters):

	sales_partner = filters.get("sales_partner")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	return frappe.db.sql("""
		SELECT
			t_inv.posting_date,
			CASE WHEN t_inv.customer_name IS NULL THEN 'Total for all customers' ELSE t_inv.customer_name END AS 'customer_name',
			CASE WHEN t_inv.name IS NULL THEN CONCAT('Total for ',t_inv.customer_name) ELSE t_inv.name END AS 'name',
			t_invitem.item_code,
			t_invitem.item_name,
			t_invitem.qty,
			t_invitem.rate,
			CASE WHEN t_inv.name IS NULL THEN t_inv.invoice_total ELSE t_invitem.base_amount END AS 'total',
			CASE WHEN t_inv.name IS NULL THEN NULL ELSE t_inv.commission_rate END as 'commission_rate',
			CASE WHEN t_inv.name IS NULL THEN t_inv.total_commission ELSE (t_invitem.base_amount*t_inv.commission_rate/100) END AS 'total_commission'
		FROM (
			SELECT posting_date, customer_name, name, SUM(base_net_total) AS 'invoice_total', sales_partner, commission_rate, SUM(total_commission) AS 'total_commission'
			FROM `tabSales Invoice`
			WHERE sales_partner = '{sales_partner}' AND posting_date >= %(from_date)s AND posting_date <= %(to_date)s
			GROUP BY customer_name, name WITH ROLLUP LIMIT 100 ) AS t_inv LEFT JOIN `tabSales Invoice Item` AS t_invitem
			ON t_invitem.parent = t_inv.name """.format(sales_partner=sales_partner),
			{
				"from_date": from_date,
				"to_date": to_date
			},
			as_dict=True)
