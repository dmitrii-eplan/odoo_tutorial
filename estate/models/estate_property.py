from win32ui import types

from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero



class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate property"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available from", copy=False, default = date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection = [('north', 'North'),
                                                       ('south', 'South'),
                                                       ('east', 'East'),
                                                       ('west', 'West')])
    state = fields.Selection(selection=[('new', 'New'),
                                        ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],
                                        default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0 AND expected_price > 0)',
         'A property selling price must be positive')
    ]


    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            list_of_price = [offer.price for offer in record.offer_ids]
            record.best_price = 0 if len(list_of_price) == 0 else max(list_of_price)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold_property(self):
        if self.state != "canceled":
            self.state = "sold"
        else:
            raise ValidationError("A canceled property cannot be set as sold")

    def action_cancel_property(self):
        if self.state != "sold":
            self.state = "canceled"
        else:
            raise ValidationError("A sold property cannot be canceled")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            comparing_of_prices = float_compare(record.selling_price, record.expected_price * 0.9, 2)
            if comparing_of_prices == -1: # or not float_is_zero(record.selling_price,2):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price or zero.")

    @api.ondelete(at_uninstall=False)
    def _prevent_delition_if_state(self):
        if any(property.state not in ['new','canceled'] for property in self):
            raise UserError("Can't delete a property with state New or Canceled!")