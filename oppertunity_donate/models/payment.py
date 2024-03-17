from odoo import api, fields, models,_

class Payments(models.Model):
    _name = 'payments'
    _description = 'Payments'

    name = fields.Char(string='Name',default="جديد",
        store=True,
        readonly=True)  
    source = fields.Char(string='Source')
    partner_id = fields.Many2one(string='Supporter Name', comodel_name='res.partner', ondelete='restrict', domain=[("is_supporter","=",True)])
    financial_funds_id = fields.Many2one(comodel_name='financial.funds')
    transfer_fincial_id = fields.Many2one(comodel_name='transfer.fincial')
    opportunity_donate_id = fields.Many2one(comodel_name='oppertunity.donate')
    payment_cost = fields.Float()
    net_cost = fields.Float()
    amout_deducated = fields.Float()
    frezon_cost = fields.Float()
    opportunity_donate_type_id = fields.Many2one(string='Opportunity Donate Type', comodel_name='opportunity.donate.type', ondelete='restrict')
    is_operational = fields.Boolean(string='')

    @api.model
    def create(self, vals):
        if vals.get("name", "جديد") == ("جديد"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "payment.num"
            ) or _("جديد")
        result = super(Payments, self).create(vals)
        return result
