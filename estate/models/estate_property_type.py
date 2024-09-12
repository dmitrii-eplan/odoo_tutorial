from odoo import fields, models, api


class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence ASC"

    sequence = fields.Integer(string="Sequence", default=1, help="Used to order the types")
    name = fields.Char(string="Title",required=True)
    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count",string="Offer Count")

    _sql_constraints = [
        ('property_type_name_uniq', 'unique (name)',
         'A property type name must be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)