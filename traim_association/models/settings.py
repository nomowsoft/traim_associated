# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Directorate(models.Model):
    _name = 'directorate'
    _description = 'Directorate'

    name = fields.Char()


class Zone(models.Model):
    _name = 'zone'
    _description = 'Zone'

    name = fields.Char()
    directorate_id = fields.Many2one('directorate', string='Directorate', ondelete='restrict')



class BenfictoryAttatchmentType(models.Model):
    _name = 'benfictory.attatchment.type'
    _description = 'Benfictory Attatchment Type'

    name = fields.Char()
    is_required = fields.Boolean(string='')



class BenfictoryAttatchment(models.Model):
    _name = 'benfictory.attatchment'
    _description = 'Benfictory Attatchment Type'

    
    benfictory_attatchment_type_id = fields.Many2one('benfictory.attatchment.type', string='Benfictory Attatchment Type', ondelete='restrict')
    res_partner_id = fields.Many2one('res.partner', string='Beneficiary', ondelete='restrict')
    file = fields.Binary(string='File')
    note = fields.Char(string='Note')

    @api.onchange("benfictory_attatchment_type_id")
    def _get_benfictory_attatchment_type_id(self):
        record_list = []
        for record in self :
            if record.benfictory_attatchment_type_id :
                for benfictory_attatchment in record.res_partner_id.benfictory_attatchment_ids.benfictory_attatchment_type_id:
                    record_list.append(benfictory_attatchment.id)
                return {
                    "domain": {
                        "benfictory_attatchment_type_id": "[('id', 'not in', {})]".format(record_list),
                    },
                }



class RequestAttatchmentType(models.Model):
    _name = 'request.attatchment.type'
    _description = 'Request Attatchment Type'

    name = fields.Char()
    is_required = fields.Boolean(string='')



class RequestAttatchment(models.Model):
    _name = 'request.attatchment'
    _description = 'Request Attatchment Type'

    
    request_attatchment_type_id = fields.Many2one('request.attatchment.type', string='Request Attatchment Type', ondelete='restrict')
    beneficiary_request_id = fields.Many2one('beneficiary.request', string='Beneficiary Request', ondelete='restrict')
    file = fields.Binary(string='File')
    note = fields.Char(string='Note')
    
class RequestType(models.Model):
    _name = 'request.type'
    _description = 'Request Type'

    name = fields.Char(string='Name')
    note = fields.Text(string='Note')


class Program(models.Model):
    _name = 'program'
    _description = 'Program'

    name = fields.Char(string='Name')
    note = fields.Char(string='Note')

