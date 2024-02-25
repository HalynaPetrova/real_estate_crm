from odoo import fields, models, api
from datetime import timedelta

from odoo.odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    price = fields.Float(string='Price')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    creation_date = fields.Date(string="Creation Date", default="_set_create_date")

    @api.autovacuum
    def _clean_offers(self):
        self.search([('statys', '=', 'refused')]).unlick()

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    # _sql_constraints = [
    #     ('check_validity', 'check(validity > 0)', "Date must be greater than or equal to creation")
    # ]

    @api.constrains("validity")
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError("Date must be greater than or equal to creation")

