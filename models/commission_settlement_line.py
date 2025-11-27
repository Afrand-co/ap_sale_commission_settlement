from odoo import models, fields, api


class CommissionSettlementLine(models.Model):
    _inherit = 'commission.settlement.line'

    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='فاکتور مرتبط',
        compute='_compute_invoice_id',
        store=True,
        readonly=True,
    )
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='خریدار',
        compute='_compute_partner_id',
        store=True,
        readonly=True,
    )

    @api.depends('invoice_line_id', 'object_id')
    def _compute_invoice_id(self):
        for line in self:
            invoice = False
            
            try:
                # روش 1: مستقیم از invoice_line_id
                if hasattr(line, 'invoice_line_id') and line.invoice_line_id:
                    invoice = line.invoice_line_id.move_id
            except:
                pass
            
            if not invoice:
                try:
                    # روش 2: از طریق sale order
                    if line.object_id and line.object_id._name == 'sale.order':
                        invoices = line.object_id.invoice_ids.filtered(
                            lambda inv: inv.move_type == 'out_invoice' and inv.state == 'posted'
                        )
                        if invoices:
                            invoice = invoices[0]
                except:
                    pass
            
            line.invoice_id = invoice
    
    @api.depends('invoice_id')
    def _compute_partner_id(self):
        for line in self:
            line.partner_id = line.invoice_id.partner_id if line.invoice_id else False

