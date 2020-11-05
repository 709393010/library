{
  'name': 'Library Website',
  'description': 'Create and check book checkout requests.',
  'author': 'M J Q',
  'depends': ['library_checkout','website',],
  # 'application': True,
  'data': [
            'security/library_security.xml',
            'security/ir.model.access.csv',
            'views/library_member.xml',
            'views/helloworld_template.xml',
            'views/checkout_template.xml',
            'views/website_assets.xml',
            ],
}