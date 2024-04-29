# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta, MO, SU
from odoo.exceptions import UserError
from odoo.tools import date_utils
import io
import json
import xlsxwriter


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
    custom_start_date = fields.Date(string="Custom start date")
    custom_end_date = fields.Date(string="Custom end date")
    select = fields.Selection(selection=[
        ("class", "Class"),
        ("student", "Student")], default="class")
    class_id = fields.Many2one("school.class", string='class')
    today = fields.Date.today()
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company.id)

    def leave_query(self):
        query = """select school_student.sequence, school_student.name, school_class.name as class,
                        school_leave.start_date,reason,end_date
                        from school_leave
                        inner join school_student on school_leave.student_id = school_student.id
                        inner join school_class on school_leave.student_class = school_class.id """
        if self.date:
            if self.date == 'day':
                query += """where '%s' between school_leave.start_date and school_leave.end_date """ % (
                    fields.Date.today())
            elif self.date == 'week':
                week_start_day = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_day = fields.Date.today() + relativedelta(weekday=SU)
                query += """where school_leave.start_date between '%s' and '%s' """ % (week_start_day, week_end_day)
            elif self.date == 'month':
                start_day = fields.Date.today() + relativedelta(day=1)
                end_day = (fields.Date.today() + relativedelta(day=1, months=1))
                query += """where '%s' <= school_leave.start_date """ % start_day
                query += """and school_leave.start_date < '%s' """ % end_day
            elif self.date == 'custom':
                if self.custom_start_date and self.custom_end_date:
                    query += ("""where school_leave.start_date between '%s' and '%s' """ %
                              (self.custom_start_date, self.custom_end_date))
                elif self.custom_start_date:
                    query += ("""where school_leave.start_date between '%s' and '%s' """ %
                              (self.custom_start_date, self.today))
        if self.select:
            if self.select == 'class':
                if self.class_id.name:
                    query += """and school_class.name = '%s' """ % self.class_id.name
            elif self.select == 'student':
                if self.name.student_id:
                    query += """and school_student.name = '%s' """ % self.name.student_id.name
        if query:
            self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_leave_report(self):
        report = self.leave_query()
        data = {
            'report': report,
        }
        if report:
            return self.env.ref('school_management.action_report_school_leave').report_action(None, data=data)
        else:
            raise UserError("No matching records")

    def action_leave_xlsx_report(self):
        report = self.leave_query()
        data = {
            'report': report,
            'school': self.school_id.name
        }
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'school.leave.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Leave Excel Report',
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
        sheet.merge_range('A4:F5', 'LEAVE EXCEL REPORT', head)
        num = 1
        sheet.write('A1', 'Date', cell_format)
        sheet.write('A2', 'School', cell_format)
        sheet.write('A8', 'Serial No.', cell_format)
        sheet.write('B8', 'Sequence', cell_format)
        sheet.write('C8', 'Name', cell_format)
        sheet.write('D8', 'Leave reason', cell_format)
        sheet.write('E8', 'Starting date', cell_format)
        sheet.write('F8', 'Ending date', cell_format)
        for i, row in enumerate(data['report'], start=9):
            sheet.write('B1', self.today, date_format)
            sheet.write('B2:C2', school, cell_format)
            sheet.write(f'A{i}', num, txt)
            sheet.write(f'B{i}', row['sequence'], txt)
            sheet.write(f'C{i}', row['name'], txt)
            sheet.write(f'D{i}', row['reason'], txt)
            sheet.write(f'E{i}', row['start_date'], txt)
            sheet.write(f'F{i}', row['end_date'], txt)
            num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



