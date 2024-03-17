from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class Project(models.Model):
    _name = 'project'
    _description = 'Project'

    name = fields.Char(string='Name')
    project_number = fields.Char(string='Project Number',default="جديد",
        store=True,
        readonly=True)
    program_ids = fields.One2many(comodel_name='program', inverse_name='project_id', string='')
    
    project_type_id = fields.Many2one(string='Project Type', comodel_name='project.type', ondelete='restrict')
    stage = fields.Selection(string='Stage', selection=[('draft', 'Draft'), ('in_progress', 'In Progress'),('done','done'),('cancel','Cancel')], default='draft')
    from_date = fields.Date(string='')
    to_date = fields.Date(string='')
    project_cost = fields.Float(string='Project Cost', compute="_compute_project_cost")
    project_place = fields.Char(string='Project Place')
    res_partner_ids = fields.One2many('res.partner', 'project_id', string='beneficiary', domain=[("is_beneficiary","=",True)])
    notes = fields.Text(string="notes")
    project_attatchment_ids = fields.One2many('project.attatchment', 'project_id', string='Project Attatchment')
    executors_ids = fields.One2many('executors', 'project_id', string='Project Attatchment')
    exchanges_ids = fields.One2many('exchanges', 'project_id', string='Exchanges')


    @api.model
    def create(self, vals):
        if vals.get("project_number", "جديد") == ("جديد"):
            vals["project_number"] = self.env["ir.sequence"].next_by_code(
                "project.num"
            ) or _("جديد")
        result = super(Project, self).create(vals)
        return result
    

    @api.constrains("project_attatchment_ids")
    def _check_project_attatchment_ids(self):
        for record in self:
            required_project_attatchment_ids = (
                self.env["project.attatchment.type"]
                .sudo()
                .search([("is_required", "=", True)])
                .ids
            )
            project_attatchment_ids = []
            required_request_attatchment_name = []
            attach = []
            for attachment_id in record.project_attatchment_ids:
                project_attatchment_ids.append(attachment_id.project_attatchment_type_id.id)
            for attachment_id in record.project_attatchment_ids:
                required_request_attatchment_name.append(attachment_id.project_attatchment_type_id.name)
            for project_attachment_id in required_project_attatchment_ids:
                if project_attachment_id not in project_attatchment_ids:
                    name = (
                        self.env["project.attatchment.type"]
                        .sudo()
                        .browse(project_attachment_id)
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


    def action_confirm(self):
        for record in self :
            record.stage = 'in_progress'

    def action_done(self):
        for record in self :
            record.stage = 'done'
    def action_cancel(self):
        for record in self :
            record.stage = 'cancel'

    @api.depends("exchanges_ids")
    def _compute_project_cost(self):
        for record in self:
                if record.exchanges_ids :
                    record.project_cost = sum(record.exchanges_ids.mapped("cost"))                    
                else:
                    record.project_cost = 0
