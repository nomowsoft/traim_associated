from odoo import api, fields, models,_

class ExchangeFund(models.Model):
    _name = 'exchange.fund'
    _description = 'Exchange Fund'

    payment_id = fields.Many2one(string='Payment', comodel_name='payments', ondelete='restrict')
    beneficiary_request_id = fields.Many2one(string='Beneficiary Request', comodel_name='beneficiary.request', ondelete='restrict')
    project_id = fields.Many2one(string='Project', comodel_name='project', ondelete='restrict')
    payment_cost = fields.Float(
        "Payment Cost", 
        related="payment_id.net_cost",
        digits=(16, 2)
    )
    amout_deducated = fields.Float(related="payment_id.amout_deducated",
        digits=(16, 2))
    frezon_cost = fields.Float(related="payment_id.frezon_cost",
        digits=(16, 2))
    cost = fields.Float()

class FinancialFunds(models.Model):
    _name = 'financial.funds'
    _description = 'Financial Funds'

    name = fields.Char(string='')

    program_id = fields.Many2one("program", string="Program")
    payment_ids = fields.One2many(
        comodel_name="payments", 
        inverse_name="financial_funds_id", 
        string="Payment"
    )
    is_operational = fields.Boolean("Is Operational")
