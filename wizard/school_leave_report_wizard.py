# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolLeaveReportWizard(models.TransientModel):
    """Model for Leave report Wizard """

    _name = "school.leave.report.wizard"
    _description = 'School Leave Report Wizard'

    name = fields.Many2one("school.leave", string="Student")
    date = fields.Selection(selection=[
        ("month", "Month"),
        ("week", "Week"),
        ("day", "Day"),
        ("custom", "Custom")], default="month")
    custom_date = fields.Date(string="Custom date")
    # custom_end_date = fields.Date(string="End date")
    select = fields.Selection(selection=[
        ("class", "Class"),
        ("student", "Student")], default="class")
    class_id = fields.Many2one("school.class", string='class')

    def action_leave_report(self):
        data = {
            'name': self.name.student_id.name,
            'date': self.date,
            'custom_date': self.custom_date,
            'select': self.select,
            'class': self.class_id.name
        }
        # docids = self.env['sale.order'].search([]).ids
        print('data from wizard', data)
        return self.env.ref('school_management.action_report_school_leave').report_action(None, data=data)

