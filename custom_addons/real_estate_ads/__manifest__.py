{
    "name": "Real Estate Ads",
    "version": "1.0",
    "author": "Halyna",
    "description": """
        Real Estate model to show available properties
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/menu_items.xml',
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
