{
    'name': "Invoice Customized",
    'summary': """
        Customization of external layout for invoices
        """,
    'category': 'Hidden',
    'version': '13.0.1.0.0',
    'author': "Luis Martínez Ontalba",
    'license': 'AGPL-3',
    "installable": True,
    'depends': [
        'account',
        'web',
    ],
    'data': [
        'data/report_paperformat.xml',
        'views/account_report.xml',
        'views/report_templates.xml',
    ]
}