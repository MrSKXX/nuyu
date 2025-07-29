{
    'name': 'POS Discount Tracker - Database Integrated',
    'version': '16.0.2.0.0',
    'category': 'Point of Sale',
    'summary': 'POS discount tracking with database integration and contact linking',
    'description': '''
POS Discount Enhancement - Database Integrated

Features:
- Complete database integration with permanent storage
- Link discount requests/approvals to actual contacts
- Advanced employee selection with search functionality
- Comprehensive discount reporting in backend
- Real-time interface updates with database status
    ''',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': [
        'point_of_sale',
        'web',
        'contacts',
    ],
    'data': [
        'views/assets.xml',
        'views/discount_reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}