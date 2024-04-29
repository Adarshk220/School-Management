# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta


class SchoolEvent(models.Model):
    """Model for Event creation and management"""
    _name = "school.event"
    _description = "School Events"
    _inherit = "mail.thread"

    name = fields.Char(required=True, string="Event Name")
    photo = fields.Binary(store=True)
    venue = fields.Char(string="Venue")
    description = fields.Html()
    clubs_id = fields.Many2one("school.club", string="Club")
    start_date = fields.Date(default=fields.date.today(), string="Start Date")
    end_date = fields.Date(default=fields.date.today(), string="End Date")
    status = fields.Selection(selection=[
        ("draft", "Draft"),
        ("registration", "Registration"),
        ("cancelled", "Cancelled")], tracking=True, default="draft")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", string="School", tracking=True,
                                 default=lambda self: self.env.company.id)

    def action_registration(self):
        """Function for the button, to change the status to registration"""

        self.status = 'registration'

    def event_reminder_email(self):
        """Function for scheduling reminder email"""
        record = self.search([])
        today = fields.Date.today()
        for rec in record:
            emailing_date = rec.start_date + timedelta(days=-2)
            if emailing_date == today:
                partners = self.env['res.partner'].search([('partner_type', 'in', ['teacher', 'staff'])])
                for partner in partners:
                    mail_template = partner.env.ref('school_management.event_email_template')
                    print(mail_template)
                    mail_template.send_mail(partner.id, force_send=True)

    def action_cancelled(self):
        """Function for button, to change the status to cancelled"""
        self.status = 'cancelled'

    def check_event(self):
        """Function to archive the expired events"""
        events = self.search([('end_date', '<', fields.Date.today())])
        for event in events:
            event.active = False

    @api.constrains("end_date", "start_date")
    def check_event_date(self):
        """Date validation of events"""
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError("Set valid dates")
