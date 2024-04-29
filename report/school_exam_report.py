# -*- coding: utf-8 -*-

from odoo import api, models


class SchoolExamReport(models.AbstractModel):
    _name = 'report.school_management.report_exam'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'data': data
        }

