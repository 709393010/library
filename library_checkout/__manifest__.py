{
    'name':'Library Book Borrowing',
    'description':'Members can borrow books from the library.',
    'author':'M J Q',
    'depends':['library_member','mail'],
    'data':[
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/checkout_view.xml',
        'views/library_checkout_stage.xml',
        'views/checkout_kanban_view.xml',
        'wizard/checkout_mass_message_wizard.xml',
    ]

}