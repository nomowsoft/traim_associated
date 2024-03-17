from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BeneficiaryRequest(models.Model):
    _name = 'beneficiary.request'
    _description = 'Beneficiary Request'

    name = fields.Char(string='Name',default="جديد",
        store=True,
        readonly=True)
    partner_id = fields.Many2one(string='Beneficiary Name', comodel_name='res.partner', ondelete='restrict', domain=[("is_beneficiary","=",True)])
    request_type_id = fields.Many2one(string='Request Type', comodel_name='request.type', ondelete='restrict')
    program_id = fields.Many2one(string='Program', comodel_name='program', ondelete='restrict')
    stage = fields.Selection(string='Stage', selection=[('draft', 'Draft'), ('in_progress', 'In Progress'),('done','done'),('cancel','Cancel')], default='draft')
    beneficiary_state_description = fields.Text()
    note = fields.Text(string="note")
    request_attatchment_ids = fields.One2many('request.attatchment', 'beneficiary_request_id', string='Request Attatchment')
    cost = fields.Float(string='Cost')
    

    @api.model
    def create(self, vals):
        if vals.get("name", "جديد") == ("جديد"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "beneficiary.request.num"
            ) or _("جديد")
        result = super(BeneficiaryRequest, self).create(vals)
        return result
    
    def action_confirm(self):
        for record in self :
            record.stage = 'in_progress'

    def action_done(self):
        for record in self :
            record.stage = 'done'

    def action_cancel(self):
        for record in self :
            record.stage = 'cancel'

    @api.constrains("request_attatchment_ids")
    def _check_request_attatchment_ids(self):
        # sdfgsdgsg
        for record in self:
            required_request_attatchment_ids = (
                self.env["request.attatchment.type"]
                .sudo()
                .search([("is_required", "=", True)])
                .ids
            )
            request_attatchment_ids = []
            required_request_attatchment_name = []
            attach = []
            for attachment_id in record.request_attatchment_ids:
                request_attatchment_ids.append(attachment_id.request_attatchment_type_id.id)
            for attachment_id in record.request_attatchment_ids:
                required_request_attatchment_name.append(attachment_id.request_attatchment_type_id.name)
            for request_attachment_id in required_request_attatchment_ids:
                if request_attachment_id not in request_attatchment_ids:
                    name = (
                        self.env["request.attatchment.type"]
                        .sudo()
                        .browse(request_attachment_id)
                        .name
                    )
                    raise ValidationError(
                        _("You Should Add Attachment :") + name
                    )
                    
                    

            for attachment in required_request_attatchment_name:
                if attachment in attach:
                    raise ValidationError(
                        _("You Can Not Allow To Add Same Attachment Type {} More Than One".format(attachment))
                    )
                else:
                    attach.append(attachment)
