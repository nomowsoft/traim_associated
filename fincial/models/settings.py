# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import re

class ProjectType(models.Model):
    _name = 'project.type'
    _description = 'Project Type'

    name = fields.Char()

class ProjectAttatchmentType(models.Model):
    _name = 'project.attatchment.type'
    _description = 'Project Attatchment Type'

    name = fields.Char()
    is_required = fields.Boolean(string='')



class ProjectAttatchment(models.Model):
    _name = 'project.attatchment'
    _description = 'Project Attatchment Type'

    
    project_attatchment_type_id = fields.Many2one('project.attatchment.type', string='Project Attatchment Type', ondelete='restrict')
    project_id = fields.Many2one('project', string='Project', ondelete='restrict')
    file = fields.Binary(string='File')
    note = fields.Char(string='Note')



class Executors(models.Model):
    _name = 'executors'
    _description = 'Executors'

    name = fields.Char(string='Name')
    mobile = fields.Char(string='Mobile')
    directorate_id = fields.Many2one('directorate', string='Directorate')
    zone_id = fields.Many2one('zone', string='Zone')
    note = fields.Text('Note')
    project_id = fields.Many2one('project', string='Project', ondelete='restrict')
    executor_type = fields.Selection(string='Executor Type', selection=[('teacher', 'Teacher'), ('administrative', 'Administrative'),])
    
    @api.constrains("mobile")
    def _check_mobile(self):
        if self.mobile:
            if not re.match(r"^[0-9]*$", self.mobile):
                raise ValidationError(_("mobile must be number"))

class ExchangeType(models.Model):
    _name = 'exchange.type'
    _description = 'ExchangeType'

    name = fields.Char(string='Name')


class Program(models.Model):
    _inherit = 'program'

    project_id = fields.Many2one(comodel_name='project', string='Project')
    

class Exchanges(models.Model):
    _name = 'exchanges'
    _description = 'ExchangeType'

    date = fields.Date(string='')
    exchange_type_id = fields.Many2one(comodel_name='exchange.type')
    cost = fields.Float(string='')
    project_id = fields.Many2one('project', string='Project', ondelete='restrict')
