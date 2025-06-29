{
    'name': 'NuYu Medical Spa - Inventory Management',
    'version': '16.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Medical spa inventory with expiry tracking, consignment, and room transfers',
    'description': '''
    Complete medical spa inventory management system featuring:
    - Multi-location inventory (Main Warehouse → Treatment Rooms)
    - Room-to-room transfer workflows
    - Consignment inventory tracking with supplier management
    - Medical product categorization (Injectable, Consumable, Retail, Device)
    - Expiry date monitoring and alerts
    - Refrigeration requirement tracking
    - Lebanese currency support (LBP)
    - Professional medical spa workflows
    ''',
    'author': 'Georges Skaf - Symufolk/Home Logic',
    'website': 'https://github.com/MrSKXX/nuyu-odoo-customizations',
    'depends': [
        'base',
        'stock',
        'product',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data Files
        'data/stock_location_data.xml',
        'data/product_category_data.xml',
        
        # Views
        'views/medical_inventory_menus.xml',
        'views/product_views.xml',
        'views/consignment_views.xml',
        'views/room_transfer_views.xml',
        'views/stock_location_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}