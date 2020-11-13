from odoo import models,fields

class LibraryRentWizard(models.TransientModel):
    _name = 'library.rent.wizard'
    _description = 'Book Rent Wizard'
    borrower_id = fields.Many2one('library.member',string='Borrower')
    book_ids = fields.Many2one('library.book',string='Books')

    #添加在临时模型上执行动作的回调方法
    def add_book_rents(self):
        rentModel = self.env['library.book.rent']
        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({
                    'borrower_id':wiz.borrower_id.id,
                    'book_id':book.id
                })