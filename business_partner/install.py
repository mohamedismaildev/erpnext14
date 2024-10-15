import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# Create custom fields for Sales Invoice and Sales Invoice Item
def create_custom_fields_for_sales_invoice():
    custom_fields = {
        'Sales Invoice': [
            {
                'fieldname': 'business_partner',
                'label': 'Business Partner',
                'fieldtype': 'Link',
                'options': 'Business Partners',
                'insert_after': 'customer'
            },
            {
                'fieldname': 'business_partner_account',
                'label': 'Business Partner Account',
                'fieldtype': 'Link',
                'options': 'Account',
                'insert_after': 'business_partner'
            },
            {
                'fieldname': 'business_partner_share',
                'label': 'Business Partner Share',
                'fieldtype': 'Currency',
                'insert_after': 'business_partner_account',
                'read_only': 1  # Make this a read-only field since it's calculated
            }
        ],
        'Sales Invoice Item': [
            {
                'fieldname': 'subject_for_shares',
                'label': 'Subject for Shares',
                'fieldtype': 'Check',
                'insert_after': 'net_amount',
                'fetch_from': 'item_code.subject_for_shares',  # Fetch the value from Item doctype
                'read_only': 1
            }
        ]
    }

    create_custom_fields(custom_fields)

# Create custom field in Item doctype
def create_custom_fields_for_item():
    custom_fields = {
        'Item': [
            {
                'fieldname': 'subject_for_shares',
                'label': 'Subject for Shares',
                'fieldtype': 'Check',
                'insert_after': 'standard_rate',
                'description': 'Check if this item is subject to business partner shares.'
            }
        ]
    }

    create_custom_fields(custom_fields)

# Create the Business Partners Doctype
def create_business_partner_doctype():
    if not frappe.db.exists('DocType', 'Business Partners'):
        business_partner = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Business Partners',
            'module': 'business_partner',
            'custom': 1,
            'fields': [
                {
                    'fieldname': 'partner_name',
                    'label': 'Partner Name',
                    'fieldtype': 'Data',
                    'reqd': 1,
                    'in_list_view': 1
                },
                {
                    'fieldname': 'partner_account',
                    'label': 'Partner Account',
                    'fieldtype': 'Link',
                    'options': 'Account',
                    'in_list_view': 1
                }
            ],
            'autoname': 'field:partner_name',
            'permissions': [{'role': 'System Manager', 'read': 1, 'write': 1, 'create': 1}]
        })
        business_partner.insert(ignore_permissions=True)
