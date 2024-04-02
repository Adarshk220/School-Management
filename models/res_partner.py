# -*- coding: utf-8 -*-


from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Model for inheritance in partner"""
    _inherit = "res.partner"


    partner_type = fields.Selection([('teacher', 'Teacher'), ('student', 'Student'),
                                     ('staff', 'Office staff')],string="Partner Type")


    @api.constrains('name', 'email')
    def _check_partner(self):
        """validation for Unique partner"""
        for record in self:
            partner_rec = self.env['res.partner'].search(
                [('name', '=', record.name), ('email', '=', record.email), ('id', '!=', record.id)])
            if partner_rec:
                raise ValidationError('Partner "' + record.name + '" already exists in Odoo!')
