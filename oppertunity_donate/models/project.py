from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project'

    project_exchange_fund_ids = fields.One2many(comodel_name='exchange.fund', inverse_name='project_id', string='Exchange Fund')
    remaining_amount = fields.Float(string='Remaint Amount', compute="_compute_project_exchange_fund_ids")

    def update_exchange_fund(self):
            if not self.program_ids:
                raise ValidationError(
                        _("You Should select programs"))
            payment_ids = []
            for exchange_fund in self.project_exchange_fund_ids:
                if (
                    exchange_fund.payment_id.net_cost == 0.0
                ):
                    exchange_fund.unlink()
                else:
                        payment_ids.append(exchange_fund.payment_id.id)
            for program in self.program_ids :
                payments = (
                    self.env["payments"]
                    .sudo()
                    .search([("financial_funds_id.name", "=", program.name),
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
                                "project_id" : self.id,
                            }
                        )
                    )

    def action_confirm(self):
        for record in self :
            if record.remaining_amount != 0:
                raise ValidationError(
                        _("Remaining Amount Should be zero")
                    )
            if record.project_cost == 0:
                raise ValidationError(
                        _("Project Cost Should be not zero")
                    )
            for exchange_fund_id in record.project_exchange_fund_ids:
                payment = exchange_fund_id.payment_id  
                payment.frezon_cost += exchange_fund_id.cost
                payment.net_cost -= exchange_fund_id.cost
            super(Project, record).action_confirm()

    def action_done(self):
        for record in self :
            for exchange_fund_id in record.project_exchange_fund_ids:
                payment = exchange_fund_id.payment_id  
                payment.frezon_cost -= exchange_fund_id.cost
                payment.amout_deducated += exchange_fund_id.cost
            super(Project, record).action_done()
    
    @api.depends("project_exchange_fund_ids","project_cost")
    def _compute_project_exchange_fund_ids(self):
        for record in self:
                if record.project_exchange_fund_ids :
                    record.remaining_amount = record.project_cost -  sum(record.project_exchange_fund_ids.mapped("cost"))
                else :
                    record.remaining_amount = record.project_cost
