{
    'name': 'HR Appraisal',
    'version': '1.0',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'author': 'Your Name',
    'depends': ['hr', 'base', 'mail'],
    'data': [
        'views/appraisal_views.xml',
        'views/appraisal_menu.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/email_templates.xml',
    ],
    'installable': True,
    'application': True
}
