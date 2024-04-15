# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolStudentReportWizard(models.TransientModel):
    """Model for Student report Wizard"""

    _name = "school.student.report.wizard"
    _description = 'School student Report Wizard'

    class_id = fields.Many2one("school.class", string='Class')
    department_id = fields.Many2one("school.department", string='Department')

    def action_student_report(self):
        data = {
            'student_class': self.class_id.name,
            'department': self.department_id.name
        }
        # docids = self.env['sale.order'].search([]).ids
        return self.env.ref('school_management.action_report_school_student').report_action(None, data=data)

