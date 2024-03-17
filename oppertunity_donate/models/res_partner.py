from odoo import api, fields, models

class Partner(models.Model):
    _inherit = "res.partner"

    is_supporter = fields.Boolean(string='')
    directorate_id = fields.Many2one('directorate', string='Directorate')
    zone_id = fields.Many2one('zone', string='Zone')
    note = fields.Text(string='Note')
        