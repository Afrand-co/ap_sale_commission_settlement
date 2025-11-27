from odoo import models, fields, api


class CommissionSettlement(models.Model):
    _inherit = 'commission.settlement'

    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='فاکتور مرتبط',
        compute='_compute_invoice_id',
        store=True,
        readonly=True,
    )
    
    invoice_ids = fields.Many2many(
        comodel_name='account.move',
        string='فاکتورهای مرتبط',
        compute='_compute_invoice_id',
        store=True,
    )
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='خریدار',
        compute='_compute_partner_id',
        store=True,
        readonly=True,
    )

    @api.depends('line_ids')
    def _compute_invoice_id(self):
        for settlement in self:
            invoices = False
            # بررسی اینکه آیا line_ids وجود دارد
            if settlement.line_ids:
                # سعی در یافتن invoice از طریق مسیرهای مختلف
                try:
                    # روش 1: مستقیم از invoice_line_id
                    first_line = settlement.line_ids[0]
                    if hasattr(first_line, 'invoice_line_id') and first_line.invoice_line_id:
                        invoices = settlement.line_ids.mapped('invoice_line_id.move_id')
                except:
                    pass
                
                if not invoices:
                    try:
                        # روش 2: از طریق sale order
                        first_line = settlement.line_ids[0]
                        if hasattr(first_line, 'object_id') and first_line.object_id:
                            invoices = settlement.line_ids.mapped('object_id.invoice_ids').filtered(
                                lambda inv: inv.move_type == 'out_invoice' and inv.state == 'posted'
                            )
                    except:
                        pass
                
                if not invoices:
                    try:
                        # روش 3: از طریق invoice_id مستقیم در line
                        first_line = settlement.line_ids[0]
                        if hasattr(first_line, 'invoice_id') and first_line.invoice_id:
                            invoices = settlement.line_ids.mapped('invoice_id')
                    except:
                        pass
            
            if invoices:
                settlement.invoice_ids = [(6, 0, invoices.ids)]
                settlement.invoice_id = invoices[0]
            else:
                settlement.invoice_ids = [(5, 0, 0)]
                settlement.invoice_id = False
    
    @api.depends('invoice_id')
    def _compute_partner_id(self):
        for settlement in self:
            if settlement.invoice_id and hasattr(settlement.invoice_id, 'partner_id'):
                settlement.partner_id = settlement.invoice_id.partner_id
            else:
                settlement.partner_id = False

