# -*- coding: utf-8 -*-

from odoo import api, models


class SchoolEventReport(models.AbstractModel):
    _name = 'report.school_management.report_event'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'data': data
        }
