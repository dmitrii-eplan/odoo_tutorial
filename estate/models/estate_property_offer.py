from datetime import timedelta, date
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float(string="Price", default=0, required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'),
                                        ('refused', 'Refused')],
                                        copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date("Deadline",compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")

    _sql_constraints = [
        ('check_number', 'CHECK(price > 0)',
         'An offer price must be strictly positive')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                   record.date_deadline = date.today()


    def _inverse_date_deadline(self):
        for record in self:
            record.date_deadline = record.date_deadline - timedelta(days=record.validity)

    def action_accept_offer(self):
        flag_for_offer = True

        for offer in self.property_id.offer_ids:
            if offer.status == "accepted":
                flag_for_offer = False
                raise ValidationError("There is already an accepted offer for this property")
                break

        if flag_for_offer:
            self.status = "accepted"
            self.property_id.buyer = self.partner_id
            self.property_id.selling_price = self.price

    def action_refuse_offer(self):
        self.status = "refused"

    @api.model
    def create(self, vals):
        current_property = self.env['estate.property'].browse(vals['property_id'])
        best_offer_price = 0

        if len(current_property.offer_ids) > 0:
            best_offer_price = max([offer.price for offer in current_property.offer_ids])

        if best_offer_price > vals['price']:
            raise UserError(f"Not allowed to create an offer with a lower amount than an existing offer.")
        else:
            current_property.state = 'offer_received'

        return super(estate_property_offer,self).create(vals)