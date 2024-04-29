from datetime import datetime
from odoo import fields
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
import base64


class StudentWebsite(http.Controller):
    @http.route(['/student_web_form'], type='http', auth="user", website=True)
    def student(self):
        class_id = request.env['school.class'].sudo().search([])
        values = {
            'class': class_id
        }
        return request.render("school_management.online_student_registration_form", values)

    @http.route(['/student_registration'], type='http', auth="public", website=True, csrf=False)
    def action_create_student(self, **ss):
        """ Student Creation"""
        name = ss.get('name')
        last_name = ss.get('last_name')
        phone = ss.get('phone')
        email = ss.get('email')
        class_id = ss.get('class_id')
        dob_string = ss.get('dob')
        dob = datetime.strptime(dob_string, '%Y-%m-%d')
        gender = ss.get('gender')
        communication_add = ss.get('communication_add')
        same = ss.get('same')
        permanent_add = ss.get('permanent_add')
        age = (fields.datetime.today() - dob).days / 365
        if same == 'on':
            active = True
        else:
            active = False
        if age < 1:
            raise ValidationError('Invalid DOB')
        request.env['school.student'].create({
            'name': name,
            'last_name': last_name,
            'communication_add': communication_add,
            'permanent_add': permanent_add,
            'email': email,
            'student_class_id': class_id,
            'phone': phone,
            'dob': dob,
            'gender': gender,
            'same': active
        })
        return request.render('school_management.thank_you_form')


class LeaveWebsite(http.Controller):
    @http.route(['/leave_web_form'], type='http', auth="public", website=True, csrf=False)
    def leave(self):
        student = request.env['school.student'].search([])

        values = {
            'students': student,
        }
        return request.render(
            "school_management.online_leave_registration_form", values)

    @http.route(['/leave_registration'], type='http', auth="public", website=True, csrf=False)
    def action_create_leave(self, **sl):
        """Leave Creation"""
        start_date = sl.get('start_date')
        end_date = sl.get('end_date')
        reason = sl.get('reason')
        student_id = sl.get('student_id')
        if start_date > end_date:
            raise ValidationError('End date must be greater than start date')
        request.env['school.leave'].create({
            'student_id': student_id,
            'start_date': start_date,
            'end_date': end_date,
            'reason': reason,
        })
        return request.render('school_management.thank_you_form')


class EventWebsite(http.Controller):
    @http.route(['/event_web_form'], type='http', auth="user", website=True)
    def event(self):
        club = request.env['school.club'].sudo().search([])
        values = {
            'clubs': club
        }

        return request.render("school_management.online_event_registration_form", values)

    @http.route(['/event_registration'], type='http', auth="public", website=True, csrf=False)
    def action_create_event(self, **se):
        """ Event Creation"""
        name = se.get('name')
        venue = se.get('venue')
        club = se.get('club_id')
        start_date = se.get('start_date')
        end_date = se.get('end_date')
        description = se.get('description')
        attachment = se.get('attachment').read()
        photo = base64.b64encode(attachment)
        if end_date <= start_date:
            raise ValidationError("End date must be greater than start date")

        request.env['school.event'].create({
            'name': name,
            'venue': venue,
            'clubs_id': club,
            'start_date': start_date,
            'end_date': end_date,
            'description': description,
            'photo': photo,
        })
        return request.render('school_management.thank_you_form')
