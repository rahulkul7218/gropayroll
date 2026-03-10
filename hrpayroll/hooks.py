app_name = "hrpayroll"
app_title = "hrpayroll"
app_publisher = "rahul"
app_description = "hrpayroll"
app_email = "abcd@gmail.com"
app_license = "mit"


after_migrate = [
    "hrpayroll.patches.add_custom_employee_fields.execute"
]

doctype_js = {

}


doc_events = {
    "Salary Slip": {
        "on_update": "hrpayroll.api.salary_slip.fetch_employee_salary_details"
    }
}