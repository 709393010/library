from odoo import models,fields,api
from odoo.exceptions import Warning

class LibraryReturnsWizard(models.TransientModel):
    _name = 'library.return.wizard'

    borrower_id = fields.Many2one('library.member',string='Member') 
    book_ids = fields.Many2many('library.book',string='Books') 


    #如果book_ids为空，则弹出提示
    @api.constrains('book_ids')
    def judge_rent_book_null(self):
        if not self.book_ids :
            raise models.ValidationError('Return book is Null !')

    #自动填充book_ids
    @api.onchange('borrower_id')
    def onchange_member(self):
        rentModel = self.env['library.book.rent']
        books_on_rent = rentModel.search(
            [('state','=','ongoing'),
            ('borrower_id.name','=',self.borrower_id.name)]) #判断借阅列表的name = 会员列表的name
        self.book_ids = books_on_rent.mapped('book_id')
        

    #修改state为returned
    @api.multi
    def	return_books(self):
        returnModel = self.env['library.book.rent']
        books_on_return = returnModel.search(
            [('state','=','ongoing'),
            ('borrower_id.name','=',self.borrower_id.name)]
        )
        books_on_return.write({'state' : 'returned'})
        #修改后跳转到Book Rent view
        return {
            'type' : 'ir.actions.act_window',
            'res_model' : 'library.book.rent',
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'target' : 'new'
        }