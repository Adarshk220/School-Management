# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from odoo.exceptions import UserError
from odoo.tools import date_utils
import io
import json
import xlsxwriter


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
    today = fields.Date.today()
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company.id)

    def event_query(self):
        date = self.date
        custom_date = self.custom_date
        club = self.club_id.name

        query = """select school_event.start_date,end_date,school_club.name as club,school_event.name
                        from school_event
                        inner join school_club on school_event.clubs_id = school_club.id """

        if date:
            if date == 'day':
                query += """where '%s' between school_event.start_date and school_event.end_date """ % (
                    fields.Date.today())
            elif date == 'week':
                week_start_day = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_day = fields.Date.today() + relativedelta(weekday=SU)
                query += """where school_event.start_date between '%s' and '%s' """ % (week_start_day, week_end_day)
            elif date == 'month':
                start_day = fields.Date.today() + relativedelta(day=1)
                end_day = fields.Date.today() + relativedelta(day=1, months=1) + timedelta(-1)
                query += """where school_event.start_date between '%s' and '%s' """ % (start_day, end_day)
            else:
                if custom_date:
                    query += """where '%s' between school_event.start_date and school_event.end_date """ % custom_date
                else:
                    raise UserError("Set Custom date")
        if club:
            query += """and school_club.name = '%s' """ % club

        if query:
            self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_event_report(self):
        report = self.event_query()
        data = {
            'report': report,
            'date': self.date,
            'custom_date': self.custom_date,
            'club': self.club_id.name
        }
        if report:
            return self.env.ref('school_management.action_report_school_event').report_action(None, data=data)
        else:
            raise UserError("No matching records")

    def action_event_xlsx_report(self):
        report = self.event_query()
        data = {
            'report': report,
            'school': self.school_id.name
        }
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'school.event.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Event Excel Report',
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
        sheet.merge_range('A4:F5', 'EVENT EXCEL REPORT', head)
        num = 1
        sheet.write('A1', 'Date', cell_format)
        sheet.write('A2', 'School', cell_format)
        sheet.write('A8', 'Serial No.', cell_format)
        sheet.write('B8', 'Event name', cell_format)
        sheet.write('C8', 'Club', cell_format)
        sheet.write('D8', 'Starting date', cell_format)
        sheet.write('E8', 'Ending date', cell_format)
        for i, row in enumerate(data['report'], start=9):
            sheet.write('B1', self.today, date_format)
            sheet.write('B2:C2', school, cell_format)
            sheet.write(f'A{i}', num, txt)
            sheet.write(f'B{i}', row['name'], txt)
            sheet.write(f'C{i}', row['club'], txt)
            sheet.write(f'D{i}', row['start_date'], txt)
            sheet.write(f'E{i}', row['end_date'], txt)
            num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
