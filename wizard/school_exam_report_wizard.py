# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils
import io
import json
import xlsxwriter


class SchoolExamReportWizard(models.TransientModel):
    """Model for Exam report Wizard"""

    _name = "school.exam.report.wizard"
    _description = 'School Exam Report Wizard'

    student_id = fields.Many2one("school.student", string='Student')
    class_id = fields.Many2one("school.class", string='Class')
    today = fields.Date.today()
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company.id)

    def exam_query(self):
        student = self.student_id.name
        exam_class = self.class_id.name

        query = """ select school_subject.name as subject,school_exam_paper.subject_name_id,school_exam.name,
                        school_student.name as student,school_class.name as class
                        from school_exam
                        inner join school_class on school_exam.student_exam_class_id = school_class.id
                        inner join school_student on school_class.id = school_student.student_class_id
                        inner join school_exam_paper on school_exam.id = school_exam_paper.student_exam_id
                        inner join school_subject on school_exam_paper.subject_name_id = school_subject.id """

        if self.student_id:
            query += """where school_student.name = '%s' """ % student
        if self.class_id:
            query += """and school_class.name = '%s' """ % exam_class
        if query:
            self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_exam_report(self):
        report = self.exam_query()
        data = {
            'report': report,
            'exam_class': self.class_id.name,
            'student': self.student_id.name
        }
        if report:
            return self.env.ref('school_management.action_report_school_exam').report_action(None, data=data)
        else:
            raise UserError("No matching records")

    def action_exam_xlsx_report(self):
        report = self.exam_query()
        data = {
            'report': report,
            'school': self.school_id.name
        }
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'school.exam.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Exam Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise UserError("No matching records")

    def get_xlsx_report(self, data, response):

        school = data.get('school')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '8px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.set_column('A:Q', 20)
        date_format = workbook.add_format(
            {'font_size': '7px', 'align': 'center', 'num_format': 'mm/dd/yyyy', 'bold': True})
        sheet.merge_range('A4:F5', 'EXAM EXCEL REPORT', head)
        num = 1
        sheet.write('A1', 'Date', cell_format)
        sheet.write('A2', 'School', cell_format)
        sheet.write('A8', 'Serial No.', cell_format)
        sheet.write('B8', 'Exam', cell_format)
        sheet.write('C8', 'Student', cell_format)
        sheet.write('D8', 'Class', cell_format)
        sheet.write('E8', 'Subject', cell_format)
        for i, row in enumerate(data['report'], start=9):
            sheet.write('B1', self.today, date_format)
            sheet.write('B2:C2', school, cell_format)
            sheet.write(f'A{i}', num, txt)
            sheet.write(f'B{i}', row['name'], txt)
            sheet.write(f'C{i}', row['student'], txt)
            sheet.write(f'D{i}', row['class'], txt)
            sheet.write(f'E{i}', row['subject'], txt)
            num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

