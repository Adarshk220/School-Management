# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolClass(models.Model):
    """Model for Class management"""
    _name = "school.class"
    _description = "School Class"
    _inherit = "mail.thread"

    name = fields.Char(required=True,
                       string="Class")
    department_id = fields.Many2one("school.department")
    hod_id = fields.Many2one(related="department_id.hod_id", string="Head of the department")
    student_ids = fields.One2many("school.student", "student_class_id", string="Students")
