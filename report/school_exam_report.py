# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError


class SchoolExamReport(models.AbstractModel):
    _name = 'report.school_management.report_exam'

    @api.model
    def _get_report_values(self, docids, data=None):
        student = data.get('student')
        exam_class = data.get('exam_class')

        query = """ select school_subject.name as subject,school_exam_paper.subject_name_id,school_exam.name,
                school_student.name as student,school_class.name as class
                from school_exam
                inner join school_class on school_exam.student_exam_class_id = school_class.id
                inner join school_student on school_class.id = school_student.student_class_id
                inner join school_exam_paper on school_exam.id = school_exam_paper.student_exam_id
                inner join school_subject on school_exam_paper.subject_name_id = school_subject.id """

        if student:
            query += """where school_student.name = '%s' """ % student
        if exam_class:
            query += """and school_class.name = '%s' """ % exam_class
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        print('result of exam query', result)
        if result:
            return {
                'data': result
            }
        else:
            raise UserError("No matching records")
