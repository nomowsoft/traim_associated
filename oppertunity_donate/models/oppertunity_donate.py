from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class OppertunityDonate(models.Model):
    _name = 'oppertunity.donate'
    _description = 'Oppertunity Donate'

    name = fields.Char(string='Name',default="جديد",
        store=True,
        readonly=True)    
    partner_id = fields.Many2one(string='Supporter Name', comodel_name='res.partner', ondelete='restrict', domain=[("is_supporter","=",True)])
    opportunity_donate_type_id = fields.Many2one(string='Opportunity Donate Type', comodel_name='opportunity.donate.type', ondelete='restrict')
    program_donate_ids = fields.One2many(comodel_name='program.donate', inverse_name='oppertunity_donate_id', string='Program Donate')
    stage = fields.Selection(string='Stage', selection=[('draft', 'Draft'), ('in_progress', 'In Progress'),('done','done'),('cancel','Cancel')], default='draft')
    received_date = fields.Date(string='')
    support_cost = fields.Float(string='Support Cost')
    association_percentage = fields.Float(string='Association Percentage')
    association_cost = fields.Float(string='Association Cost', compute='_compute_association_percentage')
    net_cost = fields.Float(string='Net Cost', compute='_compute_association_percentage')
    remaining_amount = fields.Float(string='Remaining Amount', compute='_compute_program_donate_cost')
    notes = fields.Text(string="notes")
    attatchment_ids = fields.One2many(comodel_name='ir.attachment', inverse_name='oppertunity_donate_id', string='')
    payments_ids = fields.One2many(comodel_name='payments', inverse_name='opportunity_donate_id', string='Payments')
    
    @api.model
    def create(self, vals):
        if vals.get("name", "جديد") == ("جديد"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "oppertunity.donate.num"
            ) or _("جديد")
        result = super(OppertunityDonate, self).create(vals)
        return result


    @api.depends("support_cost","association_percentage")
    def _compute_association_percentage(self):
        for record in self:
                record.association_cost = 0
                if 0 <= record.association_percentage <= 100:
                    association_cost = 0
                    percentage = (record.association_percentage / 100.0)
                    association_cost = round((record.support_cost * percentage), 2)
                    record.write({
                        "association_cost" : association_cost,
                        "net_cost" : record.support_cost -  association_cost, 
                    })
                else:
                    raise ValidationError(
                        _("The you should add percentage between 0 - 100")
                    )
    
    @api.depends("program_donate_ids","support_cost","association_percentage")
    def _compute_program_donate_cost(self):
        for record in self:
                record.remaining_amount = 0
                if record.program_donate_ids :
                    for program_donate in record.program_donate_ids:
                        if program_donate.cost > 0 :
                            record.remaining_amount = record.net_cost -  sum(record.program_donate_ids.mapped("cost"))
                else :
                    record.remaining_amount = record.net_cost

    @api.constrains("program_donate_ids")
    def _check_program_donate_ids(self):
        program_donates = []
        for record in self:
                if record.program_donate_ids :
                    for program_donate in record.program_donate_ids:
                        if  program_donate.cost <= 0:
                            raise ValidationError(
                                _("The you should add cost begger than 0 of program {}".format(program_donate.program_id.name))
                            )
                        if program_donate.program_id.name in program_donates:
                            raise ValidationError(
                                _("You Can Not Allow To Add Same Program {} More Than One".format(program_donate.program_id.name))
                            )
                        else:
                            program_donates.append(program_donate.program_id.name)   

    @api.constrains("remaining_amount")
    def _check_remaining_amount(self):
        for record in self:
            if  record.remaining_amount > 0:
                raise ValidationError(
                    _("remaining amout should be zero")
                )    

    def action_confirm(self):
        for record in self :
            if record.support_cost <=0:
                raise ValidationError(_("Support cost Should be bigger than zero"))
            record.stage = 'in_progress'

    def action_done(self):
        for record in self :
            if record.association_cost >0 :
                record.create_association_payment()
            if record.program_donate_ids :
                for program_donate in record.program_donate_ids :
                    record.create_limited_payment(program_donate.cost,program_donate.program_id)
            record.stage = 'done'

    def action_cancel(self):
        for record in self :
            record.stage = 'cancel'

    def create_association_payment(self):
        for record in self :
            financial_funds_id = (
                self.env["financial.funds"]
                .sudo()
                .search([("is_operational", "=", True)], limit=1)
            )
            if not financial_funds_id:
                financial_funds_id = (
                    self.env["financial.funds"]
                    .sudo()
                    .create(
                        {
                            "name": _("Operational"),
                            "is_operational": True,
                        }
                    )
                )
            self.env["payments"].create(
                {
                    "source": record.name,
                    "partner_id": record.partner_id.id,
                    "payment_cost": round(record.association_cost, 2),
                    "net_cost": round(record.association_cost, 2),
                    "financial_funds_id": financial_funds_id.id,
                    "opportunity_donate_id": record.id,
                    "opportunity_donate_type_id": record.opportunity_donate_type_id.id,
                    "is_operational" : True
                }
            )
            
    def create_limited_payment(self,cost,program_id):
            financial_funds_id = (
                self.env["financial.funds"]
                .sudo()
                .search([("program_id", "=", program_id.id)], limit=1)
            )
            if not financial_funds_id:
                financial_funds_id = (
                    self.env["financial.funds"]
                    .sudo()
                    .create(
                        {
                            "name": program_id.name,
                            "program_id": program_id.id,
                        }
                    )
                )
            self.env["payments"].create(
                {
                    "source": self.name,
                    "partner_id": self.partner_id.id,
                    "payment_cost": round(cost, 2),
                    "net_cost": round(cost, 2),
                    "financial_funds_id": financial_funds_id.id,
                    "opportunity_donate_id": self.id,
                    "opportunity_donate_type_id": self.opportunity_donate_type_id.id,
                }
            )
