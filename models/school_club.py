# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolClubs(models.Model):
    """Model for Club management"""
    _name = "school.club"
    _description = "School Clubs"
    _inherit = "mail.thread"

    name = fields.Char(required=True, string="Club")
    student_ids = fields.Many2many("school.student", required=True, string="Students", store=True)
    event_count = fields.Integer(compute='_compute_count')
    company_id = fields.Many2one("res.company", string="School", tracking=True,
                                 default=lambda self: self.env.company.id)

    def get_events(self):
        """Function for, smart button for the events in the club"""
        for record in self:
            return {
                'name': 'events',
                'view_mode': 'tree',
                'res_model': 'school.event',
                'type': 'ir.actions.act_window',
                'domain': [('clubs_id', '=', record.id)],
            }

    def _compute_count(self):
        """Function for, to find the count of events in the club(smart button)"""
        for record in self:
            record.event_count = self.env['school.event'].search_count([('clubs_id', '=', record.id)])
