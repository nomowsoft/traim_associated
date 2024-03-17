from odoo import api, fields, models

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    oppertunity_donate_id = fields.Many2one(comodel_name='oppertunity.donate', string='')
