# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpportunityDonateType(models.Model):
    _name = 'opportunity.donate.type'
    _description = 'Opportunity Donate Type'

    name = fields.Char()


class ProgramDonate(models.Model):
    _name = 'program.donate'
    _description = 'Program Donate'

    program_id = fields.Many2one(string='Program', comodel_name='program', ondelete='restrict')
    oppertunity_donate_id = fields.Many2one(string='Oppertunity Donate', comodel_name='oppertunity.donate', ondelete='restrict')
    cost = fields.Float(string='')