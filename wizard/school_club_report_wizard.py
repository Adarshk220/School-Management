# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolClubReportWizard(models.TransientModel):
    """Model for Club report Wizard"""

    _name = "school.club.report.wizard"
    _description = 'School Club Report Wizard'

    club_id = fields.Many2one("school.club", string='Club')
    student_ids = fields.Many2many("school.student", string='Student')

    def action_club_report(self):
        data = {
            'club': self.club_id.name,
            'student': self.student_ids.ids
        }
        # docids = self.env['sale.order'].search([]).ids
        print('data from event wizard', data)
        return self.env.ref('school_management.action_report_school_club').report_action(None, data=data)

