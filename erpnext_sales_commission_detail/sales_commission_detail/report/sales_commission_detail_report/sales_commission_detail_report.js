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
	],
	"formatter": function (value, row, column, data, default_formatter) {
		var value = default_formatter(value, row, column, data);
			if (data["name"]){
				if (data["name"].includes("Total for")) {
					value= "<span style='font-weight:bold'>" + value + "</span>";
				};
			}
			else {
				value = value;
			}
			return value;
		}
}
