# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError


class SchoolClubReport(models.AbstractModel):
    _name = 'report.school_management.report_club'

    @api.model
    def _get_report_values(self, docids, data=None):
        club = data.get('club')
        student = data.get('student')
        print(student)
        student_name = []
        for i in student:
            name = self.env['school.student'].browse(i).name
            student_name.append(name)
        count = len(student_name)
        print("std ids", student)
        print("std name", student_name)

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
                    query_c += """where sc.name = '%s' and ss.id = '%s'  """ % (club, student[0])
                else:
                    query_c += """where sc.name = '%s' and ss.id in %s  """ % (club, (str(tuple(student))))
            elif club:
                query_a += """where school_club.name = '%s' """ % club
            elif student:
                if count == 1:
                    query_b += """where ss.id = '%s' """ % student[0]
                else:
                    query_b += """where ss.id in %s """ % (str(tuple(student)))
        self.env.cr.execute(query_b)
        result_students = self.env.cr.dictfetchall()
        self.env.cr.execute(query_c)
        result_events = self.env.cr.dictfetchall()
        self.env.cr.execute(query_a)
        result = self.env.cr.dictfetchall()

        if result or result_students:
            return {
                'data': result,
                'data_students': result_students,
                'result_events': result_events,
                'club': club,
                'student': student,
                'count': count
            }
        else:
            raise UserError("No matching records")
