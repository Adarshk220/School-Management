# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils
import io
import json
import xlsxwriter


class SchoolClubReportWizard(models.TransientModel):
    """Model for Club report Wizard"""

    _name = "school.club.report.wizard"
    _description = 'School Club Report Wizard'

    club_id = fields.Many2one("school.club", string='Club')
    student_ids = fields.Many2many("school.student", string='Student')
    today = fields.Date.today()
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company.id)

    def action_club_report(self):
        data = {
            'club': self.club_id.name,
            'student': self.student_ids.ids,
        }
        return self.env.ref('school_management.action_report_school_club').report_action(None, data=data)

    def action_club_xlsx_report(self):
        club = self.club_id
        club_name = self.club_id.name
        student = self.student_ids
        student_ids = self.student_ids.ids
        count = len(student)
        query_a = """select school_club.name as club,school_student.name as student,school_event.name as event
                from school_club_school_student_rel
                inner join school_club on school_club_school_student_rel.school_club_id = school_club.id
                inner join school_student on school_club_school_student_rel.school_student_id = school_student.id
                inner join school_event on school_event.clubs_id = school_club.id """

        query_b = """select sc.name as club,ss.name as student,ss.phone,ss.gender,ss.dob from school_club as sc
                inner join school_club_school_student_rel on sc.id = school_club_school_student_rel.school_club_id
                inner join school_student as ss on school_club_school_student_rel.school_student_id = ss.id """

        query_c = """select se.name as event,start_date,end_date,venue,sc.name as club,ss.name as student
                from school_club as sc
                inner join school_event as se on sc.id = se.clubs_id
                inner join school_club_school_student_rel on sc.id = school_club_school_student_rel.school_club_id
                inner join school_student as ss on school_club_school_student_rel.school_student_id = ss.id """

        if student or club:
            if student and club:
                if count == 1:
                    query_c += """where sc.name = '%s' and ss.id = '%s'  """ % (club_name, student_ids[0])
                else:
                    query_c += """where sc.name = '%s' and ss.id in %s  """ % (club_name, (str(tuple(student_ids))))
            elif club:
                query_a += """where school_club.name = '%s' """ % club_name
            elif student:
                if count == 1:
                    query_b += """where ss.id = '%s' """ % student_ids[0]
                else:
                    query_b += """where ss.id in %s """ % (str(tuple(student_ids)))
        self.env.cr.execute(query_b)
        report_students = self.env.cr.dictfetchall()
        self.env.cr.execute(query_c)
        report_events = self.env.cr.dictfetchall()
        self.env.cr.execute(query_a)
        report = self.env.cr.dictfetchall()
        data = {
            'report': report,
            'report_students': report_students,
            'report_events': report_events,
            'student_id': student_ids,
            'club_id': club.id,
            'count': count,
            'school_id': self.school_id.name
        }
        if report or report_students or report_events:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'school.club.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Club Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise UserError("No matching records")

    def get_xlsx_report(self, data, response):
        student_id = data.get('student_id')
        club_id = data.get('club_id')
        count = data.get('count')
        school_id = data.get('school_id')
        student = self.env['school.student'].browse(student_id)
        club = self.env['school.club'].browse(club_id)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '8px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        sub_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.set_column('A:Q', 20)
        date_format = workbook.add_format({'font_size': '7px', 'align': 'center', 'num_format': 'mm/dd/yyyy', 'bold': True})
        sheet.merge_range('A4:F5', 'CLUB EXCEL REPORT', head)
        num = 1
        if student or club:
            if student and club:
                if count > 1:
                    sheet.write('A1', 'Date', cell_format)
                    sheet.write('A2', 'School', cell_format)
                    sheet.write('A8', 'Serial No.', cell_format)
                    sheet.write('B8', 'Student', cell_format)
                    sheet.write('C8', 'Event', cell_format)
                    sheet.write('D8', 'Club', cell_format)
                    sheet.write('E8', 'Venue', cell_format)
                    sheet.write('F8', 'Start Date', cell_format)
                    sheet.write('G8', 'End date', cell_format)
                    for i, row in enumerate(data['report_events'], start=9):
                        sheet.write('B1', self.today, date_format)
                        sheet.write('B2:C2', school_id, cell_format)
                        sheet.write(f'A{i}', num, txt)
                        sheet.write(f'B{i}', row['student'], txt)
                        sheet.write(f'C{i}', row['event'], txt)
                        sheet.write(f'D{i}', row['club'], txt)
                        sheet.write(f'E{i}', row['venue'], txt)
                        sheet.write(f'F{i}', row['start_date'], txt)
                        sheet.write(f'G{i}', row['end_date'], txt)
                        num += 1
                if count == 1:
                    sheet.write('A1', 'Date', cell_format)
                    sheet.write('A2', 'School', cell_format)
                    sheet.write('A8', 'Serial No.', cell_format)
                    sheet.write('B8', 'Event', cell_format)
                    sheet.write('C8', 'Club', cell_format)
                    sheet.write('D8', 'Venue', cell_format)
                    sheet.write('E8', 'Start Date', cell_format)
                    sheet.write('F8', 'End date', cell_format)
                    for i, row in enumerate(data['report_events'], start=9):
                        sheet.merge_range('C6:D6', row['student'], sub_head)
                        sheet.write('B1', self.today, date_format)
                        sheet.write('B2:C2', school_id, cell_format)
                        sheet.write(f'A{i}', num, txt)
                        sheet.write(f'B{i}', row['event'], txt)
                        sheet.write(f'C{i}', row['club'], txt)
                        sheet.write(f'D{i}', row['venue'], txt)
                        sheet.write(f'E{i}', row['start_date'], txt)
                        sheet.write(f'F{i}', row['end_date'], txt)
                        num += 1
            elif club:
                sheet.write('A1', 'Date', cell_format)
                sheet.write('A2', 'School', cell_format)
                sheet.write('A8', 'Serial No.', cell_format)
                sheet.write('B8', 'Student', cell_format)
                sheet.write('C8', 'Event', cell_format)
                for i, row in enumerate(data['report'], start=9):
                    sheet.merge_range('C6:D6', row['club'], sub_head)
                    sheet.write('B1', self.today, date_format)
                    sheet.write('B2:C2', school_id, cell_format)
                    sheet.write(f'A{i}', num, txt)
                    sheet.write(f'B{i}', row['student'], txt)
                    sheet.write(f'C{i}', row['event'], txt)
                    num += 1
            elif student:
                if count > 1:
                    sheet.write('A1', 'Date', cell_format)
                    sheet.write('A2', 'School', cell_format)
                    sheet.write('A8', 'Serial No.', cell_format)
                    sheet.write('B8', 'Club', cell_format)
                    sheet.write('C8', 'Student', cell_format)
                    sheet.write('D8', 'Phone', cell_format)
                    sheet.write('E8', 'Gender', cell_format)
                    sheet.write('F8', 'DOB', cell_format)
                    for i, row in enumerate(data['report_students'], start=9):
                        sheet.write('B1', self.today, date_format)
                        sheet.write('B2:C2', school_id, cell_format)
                        sheet.write(f'A{i}', num, txt)
                        sheet.write(f'B{i}', row['club'], txt)
                        sheet.write(f'C{i}', row['student'], txt)
                        sheet.write(f'D{i}', row['phone'], txt)
                        sheet.write(f'E{i}', row['gender'], txt)
                        sheet.write(f'F{i}', row['dob'], txt)
                        num += 1
                if count == 1:
                    sheet.write('A1', 'Date', cell_format)
                    sheet.write('A2', 'School', cell_format)
                    sheet.write('A8', 'Serial No.', cell_format)
                    sheet.write('B8', 'Club', cell_format)
                    sheet.write('C8', 'Phone', cell_format)
                    sheet.write('D8', 'Gender', cell_format)
                    sheet.write('E8', 'DOB', cell_format)
                    for i, row in enumerate(data['report_students'], start=9):
                        sheet.merge_range('C6:D6', row['student'], sub_head)
                        sheet.write('B1', self.today, date_format)
                        sheet.write('B2:C2', school_id, cell_format)
                        sheet.write(f'A{i}', num, txt)
                        sheet.write(f'B{i}', row['club'], txt)
                        sheet.write(f'C{i}', row['phone'], txt)
                        sheet.write(f'D{i}', row['gender'], txt)
                        sheet.write(f'E{i}', row['dob'], txt)
                        num += 1
        else:
            sheet.write('A1', 'Date', cell_format)
            sheet.write('A2', 'School', cell_format)
            sheet.write('A8', 'Serial No.', cell_format)
            sheet.write('B8', 'Club', cell_format)
            sheet.write('C8', 'Student', cell_format)
            sheet.write('D8', 'Event', cell_format)
            for i, row in enumerate(data['report'], start=9):
                sheet.write('B1', self.today, date_format)
                sheet.write('B2:C3', school_id, cell_format)
                sheet.write(f'A{i}', num, txt)
                sheet.write(f'B{i}', row['club'], txt)
                sheet.write(f'C{i}', row['student'], txt)
                sheet.write(f'D{i}', row['event'], txt)
                num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
