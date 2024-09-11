from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='salesman', string='Salesman', domain=[('state','not in',['sold','canceled','offer_accepted'])])

