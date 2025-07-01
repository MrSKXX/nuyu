{
    'name': 'NuYu Medical Spa - Appointment System',
    'version': '16.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Medical spa appointment management system',
    'description': '''
    Medical spa appointment system featuring:
    - Patient appointment booking
    - Doctor/practitioner assignment
    - Treatment room scheduling
    - Status workflow management
    - Calendar integration
    ''',
    'author': 'Symufolk/Home Logic',
    'website': 'https://github.com/MrSKXX/nuyu.git',
    'depends': [
        'base',
        'contacts',
        'calendar',
        'mail',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data Files
        'data/appointment_sequences.xml',
        
        # Views
        'views/appointment_menus.xml',
        'views/appointment_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}