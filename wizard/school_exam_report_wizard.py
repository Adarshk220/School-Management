# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolExamReportWizard(models.TransientModel):
    """Model for Exam report Wizard"""

    _name = "school.exam.report.wizard"
    _description = 'School Exam Report Wizard'

    student_id = fields.Many2one("school.student", string='Student')
    class_id = fields.Many2one("school.class", string='Class')

    def action_exam_report(self):
        data = {
            'exam_class': self.class_id.name,
            'student': self.student_id.name
        }
        # docids = self.env['sale.order'].search([]).ids
        print('data from exam wizard', data)
        return self.env.ref('school_management.action_report_school_exam').report_action(None, data=data)

