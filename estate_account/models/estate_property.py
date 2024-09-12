from odoo import models, Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        result = super().action_sold_property()

        # values_dict = {'partner_id':self.buyer.id,'move_type':'out_invoice'}
        # self.env['account.move'].create(values_dict)

        self.env['account.move'].create(
            {'partner_id': self.buyer.id, 'move_type': 'out_invoice', 'invoice_line_ids': [Command.create({
                "name": "Prise",
                "quantity": 1,
                "price_unit": self.selling_price}),
                Command.create({
                    "name": "6% of the selling price",
                    "quantity": 2,
                    "price_unit": 0.06 * self.selling_price}),
                Command.create({
                    "name": "administrative fees",
                    "quantity": 3,
                    "price_unit": 100.00})
            ], })

        return result
