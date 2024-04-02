# -*- coding: utf-8 -*-


from odoo import fields, models


class SaleOrder(models.Model):
    """Model for inheritance of status field in sale order"""
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])
