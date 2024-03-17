from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class TransferFincial(models.Model):
    _name = 'transfer.fincial'
    _description = 'Transfer Fincial'

    name = fields.Char(string='Name', default="جديد", store=True, readonly=True)
    partner_id = fields.Many2one(string='Supporter Name', comodel_name='res.partner', ondelete='restrict', domain=[("is_supporter","=",True)])
    stage = fields.Selection(string='Stage', selection=[('draft', 'Draft'), ('in_progress', 'In Progress'),('done','done')], default='draft')
    financial_funds_id = fields.Many2one(string='Financial Funds', comodel_name='financial.funds', ondelete='restrict')
    cost = fields.Float()
    remaining_amount = fields.Float(compute='_compute_transfer_request_ids', store=True)
    note = fields.Text(string='Note')
    attachment = fields.Binary('Attachment')
    transfer_request_ids = fields.One2many(comodel_name='trasfer.request', inverse_name='transfer_fincial_id', string='Trasfer Request')
    
    def action_confirm(self):
        for record in self :
            if record.remaining_amount != 0:
                raise ValidationError(
                    _("Remaining amount should be zero")
                )
            for trasfer_request in self.transfer_request_ids:
                payment = trasfer_request.payment_id  
                payment.frezon_cost += trasfer_request.transferring_cost
                payment.net_cost -= trasfer_request.transferring_cost
            record.stage = 'in_progress'

    def action_done(self):
        for record in self :
            for trasfer_request in self.transfer_request_ids:
                payment = trasfer_request.payment_id  
                payment.frezon_cost -= trasfer_request.transferring_cost
                payment.amout_deducated += trasfer_request.transferring_cost
            record.create_limited_payment()
            record.stage = 'done'
    
    def action_cancel(self):
        for record in self :
            record.stage = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get("name", "جديد") == ("جديد"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "transfer.fincial.num"
            ) or _("جديد")
        result = super(TransferFincial, self).create(vals)
        return result


    def update_financial_transfer_fund(self):
            transfer_request_ids = []
            payment_ids = []
            for trasfer_request in self.transfer_request_ids:
                if (
                    trasfer_request.payment_id.net_cost == 0.0
                ):
                    trasfer_request.unlink()
                else:
                        payment_ids.append(trasfer_request.payment_id.id)
                        transfer_request_ids.append(trasfer_request.id)
            payments = (
                self.env["payments"]
                .sudo()
                .search([("financial_funds_id", "!=", self.financial_funds_id.id),
                        ("net_cost",">",0),
                        ("is_operational","=",False),
                        ("partner_id","=",self.partner_id.id)])
            )

            for payment in payments:
                if payment.id not in payment_ids:
                    (
                        self.env["trasfer.request"]
                        .sudo()
                        .create(
                            {
                                "payment_id": payment.id,
                                "partner_id": payment.partner_id.id,
                                "financial_funds_id" : payment.financial_funds_id.id ,
                                "total_payment_cost": payment.payment_cost,
                                "transfer_fincial_id" : self.id
                            }
                        )
                    )

    def create_limited_payment(self):

            self.env["payments"].create(
                {
                    "source": self.name,
                    "partner_id": self.partner_id.id,
                    "payment_cost": round(self.cost, 2),
                    "net_cost": round(self.cost, 2),
                    "financial_funds_id": self.financial_funds_id.id,
                    "transfer_fincial_id": self.id,
                }
            )

    @api.depends("transfer_request_ids",)
    def _compute_transfer_request_ids(self):
        for record in self:
                if record.transfer_request_ids :
                    record.remaining_amount = self.cost - sum(record.transfer_request_ids.mapped("transferring_cost"))
                else :
                    record.remaining_amount = record.cost
                print("record.remaining_amount",record.remaining_amount)
    @api.constrains("cost")
    def _check_cost(self):
        for record in self:
            if record.cost <= 0:
                raise ValidationError(
                    _("cost should be bigger than zero")
                )


class TrasferRequest(models.Model):
    _name = "trasfer.request"
    _description = "Trasfer request"
    _rec_name = "payment_id"

    partner_id = fields.Many2one(string='Supporter Name', comodel_name='res.partner', ondelete='restrict', domain=[("is_supporter","=",True)])
    payment_id = fields.Many2one("payments", string="Payment")
    financial_funds_id = fields.Many2one(string='Financial Funds', comodel_name='financial.funds', ondelete='restrict')
    transfer_fincial_id = fields.Many2one(string='Transfer Fincial', comodel_name='transfer.fincial', ondelete='restrict')
    total_payment_cost = fields.Float(
        "Total Payment Cost",
        digits=(16, 2)
    )
    payment_cost = fields.Float(
        "Payment Cost", 
        related="payment_id.net_cost",
        digits=(16, 2)
    )
    amout_deducated = fields.Float(related="payment_id.amout_deducated",
        digits=(16, 2))
    frezon_cost = fields.Float(related="payment_id.frezon_cost",
        digits=(16, 2))
    transferring_cost = fields.Float("financial Claim Cost", default=0, digits=(16, 2))
    
    @api.constrains("transferring_cost")
    def _check_transferring_cost(self):
        for record in self:
            if record.transferring_cost < 0:
                raise ValidationError(_("Transferring Cost must be positive of payment {}".format(record.payment_id.name)))
            elif record.transferring_cost > record.payment_cost:
                raise ValidationError(_("Transferring Cost must be less than payment net cost in payment {}".format(record.payment_id.name)))