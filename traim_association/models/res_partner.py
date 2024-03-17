from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re
from datetime import date

class Partner(models.Model):
    _inherit = "res.partner"

    name = fields.Char(string='Name')
    is_beneficiary = fields.Boolean()
    birth_date = fields.Date()
    age = fields.Char(compute="_compute_age", store=True)
    directorate_id = fields.Many2one('directorate', string='Directorate')
    zone_id = fields.Many2one('zone', string='Zone')
    district = fields.Char('')
    mobile = fields.Char('')
    phone = fields.Char('')
    identity_type = fields.Selection(string='Identity Type', selection=[
        ('passport', 'Passport'),
        ('identity_card', 'Identity Card'),
        ('birth_certificate', 'Birth Certificate'),
        ('other', 'Other'),
        ])
    identity_number = fields.Char("Identity Number")
    identity_picture = fields.Binary(string='Identity Picture')
    benfictory_attatchment_ids = fields.One2many('benfictory.attatchment', 'res_partner_id', string='Benfictory Attatchment')

    @api.constrains("benfictory_attatchment_ids")
    def _check_benfictory_attatchment_ids(self):
        for record in self:
            required_benfictory_attatchment_ids = (
                self.env["benfictory.attatchment.type"]
                .sudo()
                .search([("is_required", "=", True)])
                .ids
            )
            benfictory_attatchment_ids = []
            benfictory_attatchment_name = []
            attach = []
            for attachment_id in record.benfictory_attatchment_ids:
                benfictory_attatchment_ids.append(attachment_id.benfictory_attatchment_type_id.id)
            for attachment_id in record.benfictory_attatchment_ids:
                benfictory_attatchment_name.append(attachment_id.benfictory_attatchment_type_id.name)
            for beneficiary_attachment_id in required_benfictory_attatchment_ids:
                if beneficiary_attachment_id not in benfictory_attatchment_ids:
                    name = (
                        self.env["benfictory.attatchment.type"]
                        .sudo()
                        .browse(beneficiary_attachment_id)
                        .name
                    )
                    raise ValidationError(
                        _("You Should Add Attachment :") + name
                    )
                    
                    

            for attachment in benfictory_attatchment_name:
                if attachment in attach:
                    raise ValidationError(
                        _("You Can Not Allow To Add Same Attachment Type {} More Than One".format(attachment))
                    )
                else:
                    attach.append(attachment)


    @api.constrains("mobile")
    def _check_mobile(self):
        if self.mobile:
            if not re.match(r"^[0-9]*$", self.mobile):
                raise ValidationError(_("mobile must be number"))
    
    @api.constrains("phone")
    def _check_phone(self):
        if self.phone:
            if not re.match(r"^[0-9]*$", self.phone):
                raise ValidationError(_("phone must be number"))

    @api.depends("birth_date")
    def _compute_age(self):
        for rec in self:
            if rec.birth_date != False:
                rec.age = date.today().year - rec.birth_date.year
            else:
                rec.age = 0

    
    @api.constrains("birth_date")
    def _check_birth_date(self):
        if self.birth_date:
            less_date = date(1901, 1, 1)
            if self.birth_date > date.today():
                raise ValidationError(
                    _("birth date should be less than or equal today")
                )
            elif self.birth_date < less_date:
                raise ValidationError(_("birth date should be correct"))