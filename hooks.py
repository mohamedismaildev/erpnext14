app_name = "business_partner"
app_title = "Business Partner"
app_publisher = "Mohamed Ismail"
app_description = "Business Partner"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "youremail@example.com"
app_license = "MIT"

doc_events = {
    "Sales Invoice": {
        "on_submit": "business_partner.business_partner.utils.sales_invoice.on_submit_sales_invoice"
    }
}

app_include_js = "/assets/business_partner/js/sales_invoice.js"
