import frappe
from erpnext.accounts.utils import get_fiscal_year
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.accounts.party import get_party_account
from erpnext.accounts.general_ledger import merge_similar_entries

def on_submit_sales_invoice(doc, method):
    # Check if business partner exists
    if not doc.business_partner:
        return

    business_partner_share = doc.business_partner_share or 0

    if business_partner_share > 0:
        create_business_partner_journal_entry(doc, business_partner_share)

def create_business_partner_journal_entry(doc, share_amount):
    # Get business partner account
    partner_account = doc.business_partner_account
    if not partner_account:
        frappe.throw("Please set a Business Partner Account for the selected Business Partner.")

    # Create a new GL Entry for Business Partner Share
    gl_entries = []

    # Get income account from sales invoice items
    income_accounts = list(set([item.income_account for item in doc.items if item.income_account]))
    if not income_accounts:
        frappe.throw("No income account found for the sales invoice items.")

    # Merge income accounts for similar entries
    income_account = income_accounts[0]  # Assuming we take the first account if there's more than one

    # Hardcode the cost center to "Main - FJ"
    hardcoded_cost_center = "Main - FJ"

    # Debit the income account for the business partner's share
    gl_entries.append(
        doc.get_gl_dict({
            "account": income_account,
            "against": partner_account,
            "debit": share_amount,
            "debit_in_account_currency": share_amount,
            "cost_center": hardcoded_cost_center,
            "project": doc.get("project"),
        })
    )

    # Credit the business partner's account
    gl_entries.append(
        doc.get_gl_dict({
            "account": partner_account,
            "against": income_account,
            "credit": share_amount,
            "credit_in_account_currency": share_amount,
            "cost_center": hardcoded_cost_center,
            "project": doc.get("project"),
        })
    )

    # Post the GL Entries
    if gl_entries:
        make_gl_entries(gl_entries, cancel=(doc.docstatus == 2), merge_entries=False)
