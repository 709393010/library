{
  'name': 'Library Management',
  'description': 'Manage library book catalogue and lending.',
  'author': 'M J Q',
  'depends': ['base'],
  'application': True,
  'data': [
            'security/library_security.xml',
            'security/ir.model.access.csv',
            'views/library_menu.xml',
            'views/book_view.xml',
            'views/book_list_template.xml',
            'views/book_rent_view.xml',
            'reports/library_book_report.xml',
            'reports/library_book_sql_report.xml',
            'LibraryRentWizard/rent_wizard_view.xml',
            'LibraryRentWizard/return_wizard_view.xml',
            ],
}