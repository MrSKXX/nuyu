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
    - Multiple calendar views (Personal, Clinic-wide, Room-based)
    - PDF-style appointment form
    - SMS/Email notifications
    - Resource management
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
    'assets': {
        'web.assets_backend': [
            'appointment_system/static/src/css/appointment_form.css',
            'appointment_system/static/src/css/calendar_styles.css',
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}