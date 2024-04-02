# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolSubject(models.Model):
    """Model for Subject management"""
    _name = "school.subject"
    _description = "School Subject"
    _inherit = "mail.thread"

    name = fields.Char(required=True, string="Subject")
    department_id = fields.Many2one("school.department", string="Department")
