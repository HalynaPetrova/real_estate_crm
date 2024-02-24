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
    ], default='new', string="Status")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available Form")
    expected_price = fields.Float(string="Expected Price", tracking=True)
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float(string="Selling Price", readonly=True)
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
    total_area = fields.Integer(string='Total Area')

    @api.onchange("living_area", "garden_area")
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type '

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag '

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
