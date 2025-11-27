{
    'name': 'AP Sale Commission Settlement Enhancement',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add related invoice to commission settlement',
    'description': """
        Adds related invoice field to commission settlement views
    """,
    'author': 'Ali Payandeh',
    'website': 'https://www.afrand.co.ir',
    'license': 'LGPL-3',
    'depends': [
        'commission',
    ],
    'data': [
        'views/commission_settlement_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

