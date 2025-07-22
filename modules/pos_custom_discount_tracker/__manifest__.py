{
    'name': 'POS Discount Tracker - Custom Module',
    'version': '16.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Custom POS discount tracking with reason and approval fields',
    'description': '''
POS Discount Enhancement

Features:
- Add discount tracking fields to POS order lines
- Track discount reason, requested by, and approved by
    ''',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': [
        'point_of_sale',
        'web',
    ],
    'data': [
        'views/assets.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}