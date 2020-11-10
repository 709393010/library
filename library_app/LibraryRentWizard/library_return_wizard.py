from odoo import models,fields,api

class LibraryReturnsWizard(models.TransientModel):
    _name = 'library.return.wizard'

    borrower_id = fields.Many2one('res.partner',string='Member')
    book_ids = fields.Many2many('library.book',string='Books')
    # name = fields.Char(related="borrower_id.borrower_id.name")

    # @api.onchange('borrower_id')
    # def _compute_res_partner(self):
    #     for record in self:
    #         print(record.borrower_id.book_id.name)
    #         record.name = record.borrower_id.book_id.name    

    #自动填充book_ids
    @api.onchange('borrower_id')
    def onchange_member(self):
        rentModel = self.env['library.book.rent']
        books_on_rent = rentModel.search(
            [('state','=','ongoing'),
            ('borrower_id','=',self.borrower_id.id)])
        self.book_ids = books_on_rent.mapped('book_id')

    #修改state为returned
    @api.multi
    def	return_books(self):
        returnModel = self.env['library.book.rent']
        books_on_return = returnModel.search(
            [('state','=','ongoing'),
            ('borrower_id','=',self.borrower_id.id)]
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