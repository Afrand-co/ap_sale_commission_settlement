from odoo import models, fields, api


class CommissionSettlement(models.Model):
    _inherit = 'commission.settlement'

    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Related Invoice',
        compute='_compute_invoice_id',
        store=True,
        readonly=True,
        help='The invoice related to this commission settlement'
    )

    @api.depends('line_ids.invoice_line_id')
    def _compute_invoice_id(self):
        """Compute the related invoice from settlement lines"""
        for settlement in self:
            # Get the first invoice from settlement lines
            invoice = settlement.line_ids.mapped('invoice_line_id.move_id')[:1]
            settlement.invoice_id = invoice if invoice else False

