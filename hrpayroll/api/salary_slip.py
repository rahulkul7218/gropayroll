import frappe
from frappe.utils import flt
 
def fetch_employee_salary_details(doc, method=None):
    """
    Fetches values from Employee master and updates the Salary Slip earnings table.
    Logic:
    - Basic: Calculated based on Payment Days / Working Days (Pro-rata).
    - Others (HRA, Special, etc.): Fixed from Employee Master (No calculation).
    """
    if not doc.employee or doc.docstatus != 0:
        return
 
    try:
        # 1. Fetch values from Employee Master
        fields = [
            "custom_basic",
            "custom_hra",
            "custom_special_allowance",
            "custom_conveyance_allowance",
            "epf",
            "esi",
            "loan",
            "tds",
            "professional_tax",
            "other_deduction",
            "misc"
        ]
       
        employee_data = frappe.db.get_value("Employee", doc.employee, fields, as_dict=True)
       
        if not employee_data:
            return
 
        # 2. Define Mapping
        earnings_mapping = {
            "Basic": "custom_basic",
            "HRA": "custom_hra",
            "Special Allowance": "custom_special_allowance",
            "Conveyance Allowance": "custom_conveyance_allowance"
        }

        deductions_mapping = {
            "EPF": "epf",
            "ESI": "esi",
            "Loan": "loan",
            "TDS": "tds",
            "Professional Tax": "professional_tax",
            "Other Deduction": "other_deduction",
            "MISC": "misc"
        }
 
        # 3. Handle Earnings
        existing_earnings = {d.salary_component: d for d in doc.earnings}
        any_updates = False
        total_days = flt(doc.total_working_days) or 1
        payment_days = flt(doc.payment_days)

        for component_name, field_name in earnings_mapping.items():
            base_amount = flt(employee_data.get(field_name))
           
            if base_amount > 0:
                if component_name in existing_earnings:
                    row = existing_earnings[component_name]
                else:
                    row = doc.append("earnings", {
                        "salary_component": component_name,
                        "abbr": frappe.db.get_value("Salary Component", component_name, "salary_component_abbr")
                    })
               
                if component_name == "Basic":
                    row.amount = (base_amount / total_days) * payment_days
                else:
                    row.amount = base_amount
               
                row.default_amount = base_amount
                any_updates = True

        # 4. Handle Deductions
        existing_deductions = {d.salary_component: d for d in doc.deductions}
        for component_name, field_name in deductions_mapping.items():
            base_amount = flt(employee_data.get(field_name))
            
            if base_amount > 0:
                if component_name in existing_deductions:
                    row = existing_deductions[component_name]
                else:
                    row = doc.append("deductions", {
                        "salary_component": component_name,
                        "abbr": frappe.db.get_value("Salary Component", component_name, "salary_component_abbr")
                    })
                
                row.amount = base_amount
                row.default_amount = base_amount
                any_updates = True
 
        if any_updates:
            # Recalculate Totals
            doc.gross_pay = 0
            for d in doc.earnings:
                doc.gross_pay += flt(d.amount)
           
            doc.total_deduction = 0
            for d in doc.deductions:
                doc.total_deduction += flt(d.amount)
               
            doc.net_pay = doc.gross_pay - doc.total_deduction
           
            # Save updates
            doc.db_update()
            for d in doc.earnings:
                d.db_update()
            for d in doc.deductions:
                d.db_update()
 
    except Exception as e:
        frappe.log_error(title="Salary Slip Custom Logic Error", message=frappe.get_traceback())
 
 