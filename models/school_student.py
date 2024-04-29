# -*- coding: utf-8 -*-

from odoo import api, fields, models, re, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SchoolStudent(models.Model):
    """Model for student registration"""
    _name = "school.student"
    _description = "School Student"
    _inherit = "mail.thread"

    name = fields.Char(string="First name")
    last_name = fields.Char(string="Last name")
    father_name = fields.Char(string="Father")
    mother_name = fields.Char(string="Mother")
    communication_add = fields.Char(string="Communication address")
    same = fields.Boolean(string="Is same as communication address ?")
    permanent_add = fields.Char(string="Permanent address")
    phone = fields.Char(string="Phone")
    dob = fields.Date(string="DOB", default=fields.date.today() + relativedelta(months=-12))
    gender = fields.Selection(selection=[("male", "Male"), ("female", "Female")])
    registration_date = fields.Datetime(default=fields.date.today(), string="Registration Date")
    previous_dep = fields.Selection(selection=[("lp", "LP"), ("up", "UP"), ("hs", "HS")],
                                    string="Previous academic department")
    previous_class = fields.Integer(string="Previous academic class")
    aadhaar = fields.Char(string="Aadhaar number")
    sequence = fields.Char(string="Sequence", default=lambda self: _('New'), readonly=True)
    status = fields.Selection(selection=[
        ("draft", "Draft"),
        ("registration", "Registration")], tracking=True, default="draft")
    photo = fields.Binary()
    tc_id = fields.Binary(string="TC")
    email = fields.Char(string="Email", required=True)
    company_id = fields.Many2one("res.company", string="School", tracking=True,
                                 default=lambda self: self.env.company.id)
    age = fields.Integer(compute="_compute_age", store=True)
    today = fields.Date(default=fields.date.today())
    club_ids = fields.Many2many("school.club", string="Clubs")
    student_class_id = fields.Many2one("school.class", string="Class")
    exam_ids = fields.One2many("school.exam", "student_exam_class_id", string="Exams")
    exam_paper_ids = fields.One2many("school.exam.paper", "student_paper_id", string="Exams")
    attendance = fields.Boolean(string="Is present", default=True, readonly=True)

    @api.model
    def create(self, vals):
        """sequence for the registered student"""
        # print(self.search([]))
        print(self)
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.student') or _('New')
        return super(SchoolStudent, self).create(vals)

    def button_registration(self):
        """Function for the button, to change the status to registration"""
        self.write({
            'status': "registration"
        })

    @api.depends("dob")
    def _compute_age(self):
        """Age calculation based on DOB"""
        for record in self:
            if record.dob:
                record.age = (record.today - record.dob).days / 365
            else:
                record.age = 0

    @api.constrains('previous_class', 'previous_dep')
    def check_previous_class(self):
        """Previous class validation based on department"""
        for record in self:
            if 0 < record.previous_class < 5 and record.previous_dep != "lp":
                raise ValidationError("Set a valid value for previous class")
            elif 5 <= record.previous_class < 8 and record.previous_dep != "up":
                raise ValidationError("Set a valid value for previous class")
            elif 8 <= record.previous_class < 11 and record.previous_dep != "hs":
                raise ValidationError("Set a valid value for previous class")

    @api.constrains('dob')
    def check_dob(self):
        """Age validation based on dob"""
        for record in self:
            if record.age <= 0:
                raise ValidationError("Set a valid DOB")

    @api.constrains('email')
    def check_email(self):
        """Email validation"""
        for record in self:
            if re.match('(\w+[.|\w])*@(\w+[.])*\w+', record.email):
                continue
            raise ValidationError("Wrong email format")

    @api.model
    def create_user(self):
        """user creation"""
        self.env['res.users'].create({
            'name': self.name,
            'login': self.email,
        })


"""Validation for Aadhaar number to be unique"""

_sql_constraints = [('Any_name', 'unique (aadhaar)', 'Enter your unique aadhaar!')]
