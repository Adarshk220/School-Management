# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from odoo.exceptions import UserError


class SchoolLeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        name = data.get('name')
        date = data.get('date')
        custom_date = data.get('custom_date')
        select = data.get('select')
        class_id = data.get('class')
        # start_day = datetime(2024, 4, 1)
        # end_day = start_day - timedelta(days=1)

        # student = self.env['school.leave'].search([('student_id.id', '=', name)])

        data_set = {
            'temp_name': name
        }
        query = """select school_student.sequence, school_student.name, school_class.name as class,
                school_leave.start_date,reason,end_date
                from school_leave
                inner join school_student on school_leave.student_id = school_student.id
                inner join school_class on school_leave.student_class = school_class.id """
        if date:
            if date == 'day':
                print("dayy")
                print(type(fields.Date.today()))
                query += """where '%s' between school_leave.start_date and school_leave.end_date """ % (fields.Date.today())
            elif date == 'week':
                week_start_day = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_day = fields.Date.today() + relativedelta(weekday=SU)
                query += """where school_leave.start_date between '%s' and '%s' """ % (week_start_day, week_end_day)
                print(week_start_day, week_end_day)
            elif date == 'month':
                start_day = fields.Date.today() + relativedelta(day=1)
                end_day = fields.Date.today() + relativedelta(day=1, months=1) + timedelta(-1)
                query += """where school_leave.start_date between '%s' and '%s' """ % (start_day, end_day)
                print('month')
                print(start_day, end_day)
            else:
                query += """where '%s' between school_leave.start_date and school_leave.end_date """ % custom_date
        if select:
            if select == 'class':
                print(type(class_id))
                query += """and school_class.name = '%s' """ % class_id
            elif select == 'student':
                print('student')
                query += """and school_student.name = '%s' """ % name
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        print('result of query', result)
        if result:
            return {
                'data': result
            }
        else:
            raise UserError("No matching records")
