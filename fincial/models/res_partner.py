from odoo import api, fields, models

class Partner(models.Model):
    _inherit = "res.partner"

    project_id = fields.Many2one('project', string='Project')
    
