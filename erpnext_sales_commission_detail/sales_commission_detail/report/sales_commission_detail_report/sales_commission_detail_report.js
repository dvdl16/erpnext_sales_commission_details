// Copyright (c) 2016, Dirk van der Laarse and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Commission Detail Report"] = {
	"filters": [
			{
					"fieldname":"sales_partner",
					"label": __("Sales Partner"),
					"fieldtype": "Link",
					"options": "Sales Partner"
			},
			{
					"fieldname":"from_date",
					"label": __("From Date"),
					"fieldtype": "Date",
					"options": ""
			},
			{
					"fieldname":"to_date",
					"label": __("To Date"),
					"fieldtype": "Date",
					"options": ""
			}
	]
}
