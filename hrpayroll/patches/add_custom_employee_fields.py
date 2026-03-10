import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	fields = {
		"Employee": [
			{
				"fieldname": "custom_basic",
				"label": "Custom Basic",
				"fieldtype": "Float",
				"insert_after": "salary_mode"
			},
			{
				"fieldname": "custom_special_allowance",
				"label": "Custom Special Allowance",
				"fieldtype": "Float",
				"insert_after": "custom_basic"
			},
			{
				"fieldname": "custom_hra",
				"label": "Custom HRA",
				"fieldtype": "Float",
				"insert_after": "custom_special_allowance"
			},
			{
				"fieldname": "custom_conveyance_allowance",
				"label": "Custom Conveyance Allowance",
				"fieldtype": "Float",
				"insert_after": "custom_hra"
			},
			{
				"fieldname": "epf",
				"label": "EPF",
				"fieldtype": "Float",
				"insert_after": "custom_conveyance_allowance"
			},
			{
				"fieldname": "esi",
				"label": "ESI",
				"fieldtype": "Float",
				"insert_after": "epf"
			},
			{
				"fieldname": "loan",
				"label": "Loan",
				"fieldtype": "Float",
				"insert_after": "esi"
			},
			{
				"fieldname": "tds",
				"label": "TDS",
				"fieldtype": "Float",
				"insert_after": "loan"
			},
			{
				"fieldname": "professional_tax",
				"label": "Professional Tax",
				"fieldtype": "Float",
				"insert_after": "tds"
			},
			{
				"fieldname": "other_deduction",
				"label": "Other Deduction",
				"fieldtype": "Float",
				"insert_after": "professional_tax"
			},
			{
				"fieldname": "misc",
				"label": "MISC",
				"fieldtype": "Float",
				"insert_after": "other_deduction"
			}
		]
	}
	create_custom_fields(fields)
