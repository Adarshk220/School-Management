# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError


class SchoolStudentReport(models.AbstractModel):
    _name = 'report.school_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        student_class = data.get('student_class')
        department = data.get('department')

        query = """select school_student.name as student,school_class.name as class,school_department.name as department
                from school_student
                inner join school_class on school_student.student_class_id = school_class.id
                inner join school_department on school_class.department_id = school_department.id """
        if student_class:
            query += """where school_class.name = '%s' """ % student_class
        if department:
            query += """and school_department.name = '%s' """ % department
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:
            return {
                'data': result
            }
        else:
            raise UserError("No matching records")
