# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils
import io
import json
import xlsxwriter


class SchoolStudentReportWizard(models.TransientModel):
    """Model for Student report Wizard"""

    _name = "school.student.report.wizard"
    _description = 'School student Report Wizard'

    class_id = fields.Many2one("school.class", string='Class')
    department_id = fields.Many2one("school.department", string='Department')
    today = fields.Date.today()
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company.id)

    def student_query(self):
        student_class = self.class_id.name,
        department = self.department_id.name
        print(student_class)

        query = """select school_student.name as student,school_class.name as class,school_department.name as department
                        from school_student
                        inner join school_class on school_student.student_class_id = school_class.id
                        inner join school_department on school_class.department_id = school_department.id """
        if self.class_id:
            query += """where school_class.name = '%s' """ % student_class
        if self.department_id:
            query += """and school_department.name = '%s' """ % department
        if query:
            print(query)
            self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_student_report(self):
        report = self.student_query()
        data = {
            'report': report,
        }
        if report:
            return self.env.ref('school_management.action_report_school_student').report_action(None, data=data)
        else:
            raise UserError("No matching records")

    def action_student_xlsx_report(self):
        report = self.student_query()
        data = {
            'report': report,
            'school': self.school_id.name
        }
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'school.student.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Student Excel Report',
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
        sheet.merge_range('A4:F5', 'STUDENT EXCEL REPORT', head)
        num = 1
        sheet.write('A1', 'Date', cell_format)
        sheet.write('A2', 'School', cell_format)
        sheet.write('A8', 'Serial No.', cell_format)
        sheet.write('B8', 'Student', cell_format)
        sheet.write('C8', 'Class', cell_format)
        sheet.write('D8', 'Department', cell_format)
        for i, row in enumerate(data['report'], start=9):
            sheet.write('B1', self.today, date_format)
            sheet.write('B2:C2', school, cell_format)
            sheet.write(f'A{i}', num, txt)
            sheet.write(f'B{i}', row['student'], txt)
            sheet.write(f'C{i}', row['class'], txt)
            sheet.write(f'D{i}', row['department'], txt)
            num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

