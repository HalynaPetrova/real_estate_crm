from odoo import fields, models, api, _


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancel')
    ], default='new', string="Status", group_expand="_expand_state")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available Form")
    expected_price = fields.Monetary(string="Expected Price", tracking=True)
    best_offer = fields.Monetary(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Monetary(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation", default='north')
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    total_area = fields.Integer(string="Total Area")
    phone = fields.Char(string='Phone', related='buyer_id.phone')
    offer_count = fields.Integer(srting="Offer Count", compute="_compute_offer_count")
    currency_id = fields.Many2one("res.currency", string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.onchange("living_area", "garden_area")
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_property_view_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": f"{self.name} - Offers",
            "domain": [("property_id", "=", self.id)],
            "view_mode": "tree",
            "res_model": "estate.property.offer",
        }

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    def _get_report_base_filename(self):
        self.ensure_one()
        return "Estate Property - %s" % self.name

    def _expand_state(self, states, domain, order):
        return [
            key for key, dummy in type(self).state.selection
        ]


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type '

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag '

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
