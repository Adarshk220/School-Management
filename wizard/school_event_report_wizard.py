# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolEventReportWizard(models.TransientModel):
    """Model for Event report Wizard"""

    _name = "school.event.report.wizard"
    _description = 'School Event Report Wizard'

    date = fields.Selection(selection=[
        ("month", "Month"),
        ("week", "Week"),
        ("day", "Day"),
        ("custom", "Custom")], default="month")
    custom_date = fields.Date(string="Custom date")
    club_id = fields.Many2one("school.club", string='club')

    def action_event_report(self):
        data = {
            'date': self.date,
            'custom_date': self.custom_date,
            'club': self.club_id.name
        }
        # docids = self.env['sale.order'].search([]).ids
        print('data from event wizard', data)
        return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)

