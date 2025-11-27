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

    @api.depends('line_ids', 'line_ids.invoice_line_id')
    def _compute_invoice_id(self):
        for settlement in self:
            invoices = settlement.line_ids.mapped('invoice_line_id.move_id')
            settlement.invoice_ids = [(6, 0, invoices.ids)]
            settlement.invoice_id = invoices[:1] if invoices else False
    
    @api.depends('line_ids', 'line_ids.invoice_line_id', 'line_ids.invoice_line_id.move_id', 'line_ids.invoice_line_id.move_id.partner_id')
    def _compute_partner_id(self):
        for settlement in self:
            # Get partner from invoice lines directly
            partners = settlement.line_ids.mapped('invoice_line_id.move_id.partner_id')
            settlement.partner_id = partners[:1] if partners else False

