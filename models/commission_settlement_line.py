from odoo import models, fields, api


class CommissionSettlementLine(models.Model):
    _inherit = 'commission.settlement.line'

    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='فاکتور مرتبط',
        compute='_compute_invoice_id',
        store=False,
        readonly=True,
    )
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='خریدار',
        compute='_compute_partner_id',
        store=False,
        readonly=True,
    )

    def _compute_invoice_id(self):
        """Compute invoice from available fields in settlement line"""
        for line in self:
            invoice = False
            
            try:
                # روش 1: مستقیم از invoice_line_id (اگر وجود داشته باشد)
                if hasattr(line, 'invoice_line_id') and line.invoice_line_id:
                    invoice = line.invoice_line_id.move_id
            except:
                pass
            
            if not invoice:
                try:
                    # روش 2: از طریق sale order (اگر object_id وجود داشته باشد)
                    if hasattr(line, 'object_id') and line.object_id:
                        if line.object_id._name == 'sale.order':
                            invoices = line.object_id.invoice_ids.filtered(
                                lambda inv: inv.move_type == 'out_invoice' and inv.state == 'posted'
                            )
                            if invoices:
                                invoice = invoices[0]
                except:
                    pass
            
            if not invoice:
                try:
                    # روش 3: از طریق invoice_id مستقیم در line (اگر وجود داشته باشد)
                    if hasattr(line, 'invoice_id') and line.invoice_id:
                        invoice = line.invoice_id
                except:
                    pass
            
            if not invoice:
                try:
                    # روش 4: از طریق settlement و سپس line_ids
                    if hasattr(line, 'settlement_id') and line.settlement_id:
                        if hasattr(line.settlement_id, 'line_ids'):
                            # سعی در یافتن invoice از سایر خطوط
                            pass
                except:
                    pass
            
            line.invoice_id = invoice
    
    def _compute_partner_id(self):
        """Compute partner from invoice"""
        for line in self:
            if line.invoice_id and hasattr(line.invoice_id, 'partner_id'):
                line.partner_id = line.invoice_id.partner_id
            else:
                line.partner_id = False

