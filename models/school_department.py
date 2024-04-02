# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolDepartment(models.Model):
    """Model for Department management"""
    _name = "school.department"
    _description = "School Department"
    _inherit = "mail.thread"

    name = fields.Char(required=True, string="Department")
    hod_id = fields.Many2one("res.partner", string="Head of the department", tracking=True)
