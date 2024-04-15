# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from odoo.exceptions import UserError


class SchoolEventReport(models.AbstractModel):
    _name = 'report.school_management.report_event'

    @api.model
    def _get_report_values(self, docids, data=None):
        date = data.get('date')
        custom_date = data.get('custom_date')
        club = data.get('club')

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
                query += """where '%s' between school_event.start_date and school_event.end_date """ % custom_date
        if club:
            print("club is here")
            query += """and school_club.name = '%s' """ % club

        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:
            return {
                'data': result
            }
        else:
            raise UserError("No matching records")
