from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BeneficiaryRequest(models.Model):
    _inherit = 'beneficiary.request'

    exchange_fund_ids = fields.One2many(comodel_name='exchange.fund', inverse_name='beneficiary_request_id', string='Exchange Fund')
    remaining_amount = fields.Float(string='Remaint Amount', compute="_compute_exchange_fund_ids")

    def update_exchange_fund(self):
            if not self.program_id:
                raise ValidationError(
                        _("You Should select program"))
            payment_ids = []
            for exchange_fund in self.exchange_fund_ids:
                if (
                    exchange_fund.payment_id.net_cost == 0.0
                ):
                    exchange_fund.unlink()
                else:
                        payment_ids.append(exchange_fund.payment_id.id)
            payments = (
                self.env["payments"]
                .sudo()
                .search([("financial_funds_id.name", "=", self.program_id.name),
                        ("net_cost",">",0),
                        ("is_operational","=",False)])
                )

            for payment in payments:
                if payment.id not in payment_ids:
                    (
                        self.env["exchange.fund"]
                        .sudo()
                        .create(
                            {
                                "payment_id": payment.id,
                                "beneficiary_request_id" : self.id
                            }
                        )
                    )

    def action_confirm(self):
        for record in self :
            if record.remaining_amount != 0:
                raise ValidationError(
                        _("Remaining Amount Should be zero")
                    )
            if record.cost == 0:
                raise ValidationError(
                        _("Cost Should be not zero")
                    )
            for exchange_fund_id in record.exchange_fund_ids:
                payment = exchange_fund_id.payment_id  
                payment.frezon_cost += exchange_fund_id.cost
                payment.net_cost -= exchange_fund_id.cost
            super(BeneficiaryRequest, record).action_confirm()


    def action_done(self):
        for record in self :
            for exchange_fund_id in record.exchange_fund_ids:
                payment = exchange_fund_id.payment_id  
                payment.frezon_cost -= exchange_fund_id.cost
                payment.amout_deducated += exchange_fund_id.cost
            super(BeneficiaryRequest, record).action_done()
    
    @api.depends("exchange_fund_ids","cost")
    def _compute_exchange_fund_ids(self):
        for record in self:
                if record.exchange_fund_ids :
                            record.remaining_amount = record.cost -  sum(record.exchange_fund_ids.mapped("cost"))
                else :
                    record.remaining_amount = record.cost
