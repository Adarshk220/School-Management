# -*- coding: utf-8 -*-

from odoo import api, models


class SchoolLeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        # date = data.get('date')
        # custom_date = data.get('custom_date')
        # select = data.get('select')
        # class_id = data.get('class')

        # query = """select school_student.sequence, school_student.name, school_class.name as class,
        #         school_leave.start_date,reason,end_date
        #         from school_leave
        #         inner join school_student on school_leave.student_id = school_student.id
        #         inner join school_class on school_leave.student_class = school_class.id """
        # if date:
        #     if date == 'day':
        #         query += """where '%s' between school_leave.start_date and school_leave.end_date """ % (fields.Date.today())
        #     elif date == 'week':
        #         week_start_day = fields.Date.today() + relativedelta(weekday=MO(-1))
        #         week_end_day = fields.Date.today() + relativedelta(weekday=SU)
        #         query += """where school_leave.start_date between '%s' and '%s' """ % (week_start_day, week_end_day)
        #     elif date == 'month':
        #         start_day = fields.Date.today() + relativedelta(day=1)
        #         end_day = fields.Date.today() + relativedelta(day=1, months=1) + timedelta(-1)
        #         query += """where school_leave.start_date between '%s' and '%s' """ % (start_day, end_day)
        #     else:
        #         query += """where '%s' between school_leave.start_date and school_leave.end_date """ % custom_date
        # if select:
        #     if select == 'class':
        #         query += """and school_class.name = '%s' """ % class_id
        #     elif select == 'student':
        #         query += """and school_student.name = '%s' """ % name
        # self.env.cr.execute(query)
        # result = self.env.cr.dictfetchall()
        return {
            'data': data,
        }
        # if report:
        #     return {
        #         'data': data
        #     }
        # else:
        #     raise UserError("No matching records")
