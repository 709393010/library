from odoo import fields,models

class LibrayBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Book Rent'
    book_id = fields.Many2one('library.book','Book',required=True)
    borrower_id = fields.Many2one('res.partner', 'Borrower',required=True)
    state = fields.Selection([('ongoing', 'Ongoing'),
                            ('returned', 'Returned'),
                            ('lost','Lost')],
                            'State', default='ongoing',
                            required=True)
    rent_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()

    #模拟图书丢失
    def book_lost(self):
        self.ensure_one()
        self.state = 'lost'
        book_with_different_context = self.book_id.with_context(avoid_deactivate=True)
        book_with_different_context.make_lost()
