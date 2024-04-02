# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta


class SchoolStaff(models.Model):
    """Model for staff management"""
    _name = "school.leave"
    _description = "School Leave"
    _inherit = "mail.thread"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.student", string="Student", required=True)
    student_class = fields.Many2one("school.class", string="Class")
    half_day = fields.Boolean(string="Half Day")
    start_date = fields.Date(default=fields.date.today(), string="Start Date")
    end_date = fields.Date(default=fields.date.today(), string="End Date")
    total_days = fields.Float(string="Total Days", compute="_compute_total_days")
    reason = fields.Html(required=True)
    company_id = fields.Many2one("res.company", string="School", tracking=True,
                                 default=lambda self: self.env.company.id)

    @api.depends("half_day", "start_date", "end_date")
    def _compute_total_days(self):
        """Calculation of total days of leave"""
        print("dam")
        for record in self:
            if record.half_day:
                record.total_days = 0.5
            elif record.end_date and record.start_date:
                total_days_count = 0
                current_date = record.start_date
                while current_date <= record.end_date:
                    if current_date.weekday() < 5:
                        total_days_count += 1
                    current_date += timedelta(days=1)
                record.total_days = total_days_count
            else:
                record.total_days = 0

    @api.constrains("start_date", "end_date")
    def check_total_days(self):
        """Total days validation"""
        for record in self:
            if record.total_days <= 0:
                raise ValidationError("Set valid dates")

    def check_attendance(self):
        """Function to check the attendance"""
        record = self.search([])
        print(record)
        today = fields.Date.today()
        for rec in record:
            print(rec)
            current_date = rec.start_date
            print(current_date)
            while current_date <= rec.end_date:
                print(current_date)
                if current_date == today:
                    rec.student_id.attendance = False
                else:
                    rec.student_id.attendance = True
                current_date += timedelta(days=1)
