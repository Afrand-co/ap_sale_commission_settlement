{
    'name': 'Sale Commission Settlement Enhancement',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add related invoice to commission settlement list view',
    'description': """
        This module extends the commission settlement to display 
        the related invoice in the list view.
    """,
    'author': 'Ali Payandeh',
    'website': 'https://www.afrand.co.ir',
    'license': 'LGPL-3',
    'depends': [
        'commission',
        'sale_commission',
    ],
    'data': [
        'views/commission_settlement_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

