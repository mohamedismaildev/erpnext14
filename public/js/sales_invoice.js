frappe.ui.form.on('Sales Invoice', {
    // Fetch the Business Partner Account when Business Partner is selected
    business_partner: function(frm) {
        if (frm.doc.business_partner) {
            // Fetch the Business Partner record
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Business Partners',
                    name: frm.doc.business_partner
                },
                callback: function(r) {
                    if (r.message) {
                        // Set the fetched partner_account in the Business Partner Account field
                        frm.set_value('business_partner_account', r.message.partner_account);
                    }
                }
            });
        }
    },
    
    validate: function(frm) {
        let total_share = 0;
        
        // Calculate Business Partner Share based on items with "Subject for Shares" checked
        frm.doc.items.forEach(function(item) {
            if (item.subject_for_shares == 1) {
                // Calculate 50% of the net amount for the items subject to shares
                total_share += (item.net_amount * 0.50);
            }
        });
        
        // Set the calculated value to the Business Partner Share field
        frm.set_value('business_partner_share', total_share);
    }
});
