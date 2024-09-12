{
    'name': 'Estate module account(tutorial)',
    'version': '1.0',
    'depends':['estate', 'account'],
    'application': True,
    'installable': True,
    'data': ['security/ir.model.access.csv',
             'views/estate_account_menus.xml',],
    'license': 'AGPL-3',
}