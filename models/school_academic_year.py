# -*- coding: utf-8 -*-


from odoo import fields, models


class SchoolAcademicYear(models.Model):
    """Model for Academic Year management"""
    _name = "school.academic.year"
    _description = "School Academic Year"

    name = fields.Char(required=True,
                       string="Academic Year")
