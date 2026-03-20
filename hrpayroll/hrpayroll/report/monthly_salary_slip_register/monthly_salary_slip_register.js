// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.query_reports["Monthly Salary Slip Register"] = {
	"filters": [
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": [
				"January", "February", "March", "April", "May", "June",
				"July", "August", "September", "October", "November", "December"
			],
			"default": ["January", "February", "March", "April", "May", "June",
				"July", "August", "September", "October", "November", "December"][new Date().getMonth()],
			"on_change": function () {
				const month = frappe.query_report.get_filter_value("month");
				if (!month) return;

				const year = frappe.datetime.get_today().split("-")[0];
				const month_idx = ["January", "February", "March", "April", "May", "June",
					"July", "August", "September", "October", "November", "December"].indexOf(month);

				// Calculate first and last day of the month
				const first_day = new Date(year, month_idx, 1);
				const last_day = new Date(year, month_idx + 1, 0);

				frappe.query_report.set_filter_value("from_date", frappe.datetime.obj_to_str(first_day));
				frappe.query_report.set_filter_value("to_date", frappe.datetime.obj_to_str(last_day));
			}
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
		}
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		const earnings = ["basic", "hra", "conv_all", "spl_all", "total_rate", "gross_salary"];
		const deductions = ["epf", "esi", "loan", "tds", "professional_tax", "other_deduction", "misc", "total_deduction"];

		if (earnings.includes(column.fieldname)) {
			value = `<span style="color: #009432; font-weight: 600;">${value}</span>`;
		} else if (deductions.includes(column.fieldname)) {
			const color = (column.fieldname === "total_deduction" || column.fieldname === "tds") ? "#eb4d4b" : "#ee5253";
			value = `<span style="color: ${color}; font-weight: 600;">${value}</span>`;
		}

		if (column.fieldname === "net_payable") {
			value = `<span style="font-weight: 700; color: #009432; font-size: 1.1em;">${value}</span>`;
		}

		return value;
	},
	"onload": function (report) {
		report.page.add_inner_button(__("Export"), function () {
			const filters = report.get_values();
			const method = "hrpayroll.hrpayroll.report.monthly_salary_slip_register.monthly_salary_slip_register.download_excel";
			const url = "/api/method/" + method + "?" + $.param({
				filters: JSON.stringify(filters)
			});
			window.open(url);
		});
	}
};
