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

    @api.depends('line_ids', 'line_ids.invoice_line_id')
    def _compute_invoice_id(self):
        for settlement in self:
            invoices = settlement.line_ids.mapped('invoice_line_id.move_id')
            settlement.invoice_ids = [(6, 0, invoices.ids)]
            settlement.invoice_id = invoices[:1] if invoices else False

