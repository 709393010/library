from odoo import fields,models,api
from odoo.exceptions import UserError
# from odoo.tools,translate import _

class CheckoutStage(models.Model):
    _name = 'library.checkout.stage'
    _description = 'Checkout Stage'
    _order = 'sequence,name'

    name = fields.Char()
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new','New'),
        ('open','Borrowed'),
        ('done','Returned'),
        ('cancel','Cancelled')],
        default='new',
    )
    #添加⼀个帮助⽅法来查看是否允许状态转换
    @api.model
    def is_allowed_transition(self,old_state,new_state):
        allowed = [('new','open'),
            ('open','done'),
            ('done','cancel'),
            ('cancel','new'),
            ('cancel','open')]
        return (old_state,new_state) in allowed

    #添加⽅法来通过调⽤change_state⽅法修改图书状态
    def make_open(self):
        self.change_state('open')
    def make_done(self):
        self.change_state('done')
    def make_cancel(self):
        self.change_state('cancel')

    #修改change_state⽅法并抛出else部分中的UserError异常
    @api.multi
    def change_state(self,new_state):
        for book in self:
            if book.is_allowed_transition(book.state,new_state):
                book.state = new_state
            else:
                msg = ('Moving from %s to %s is not allowed') % (book.state,new_state)
                raise UserError(msg)


