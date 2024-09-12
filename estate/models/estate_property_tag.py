from odoo import fields, models


class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"

    name = fields.Char(string="Title",required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('property_tag_name_uniq', 'unique (name)',
         'A property tag name must be unique')
    ]