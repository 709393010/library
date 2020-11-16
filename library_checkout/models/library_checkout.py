from odoo import api, exceptions, fields, models
class Checkout(models.Model):
    _name = 'library.checkout'
    _description = 'Checkout Request'
    _inherit = ['mail.thread','mail.activity.mixin']
    member_id = fields.Many2one(
        'library.member',
        required=True)
    user_id = fields.Many2one(
        'res.users',
        'Librarian',
        default=lambda s: s.env.uid)
    request_date = fields.Date(
        default=lambda s: fields.Date.today())
    line_ids = fields.One2many(
        'library.checkout.line',
        'checkout_id',
        string='Borrowed Books',)
    stage_id = fields.Many2one('library.checkout.stage' , string='Stage')
    checkout_date = fields.Date(default=lambda s: fields.Date.today(),readonly=True)
    close_date = fields.Date(readonly=True)
    member_image = fields.Binary(related='member_id.partner_id.image')
    num_books = fields.Integer(compute='_compute_num_books',store=True)
    
    color = fields.Integer('颜色')
    priority = fields.Selection(
        [('0','Low'),
        ('1','Normal'),
        ('2','High')],
        'Priority',
        default='1' )
    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Ready for next stage')],
        'Kanban State',
        default='normal')

    #如果stage_id=Cacelled时，清空Borrowed Books
    @api.onchange('stage_id')
    def stage_to_cacelled(self):
        if self.stage_id.name == 'Cancelled':
            self.line_ids = [(5,0,0)] #(5,0,0)清空记录集

    #更改Stage为Borrowed
    @api.multi
    def button_to_borrowed(self):
        StageModel = self.env['library.checkout.stage']
        print(StageModel.search([])[1].state)
        self.stage_id.name = StageModel.search([])[1].name
        self.stage_id.state = StageModel.search([])[1].state

    #更改Stage为Returned
    def button_to_returned(self):
        self.stage_id.name = self.env['library.checkout.stage'].search([])[2].name
        self.stage_id.state = self.env['library.checkout.stage'].search([])[2].state


    @api.depends('line_ids')
    def _compute_num_books(self):
        for book in self:
            book.num_books = len(book.line_ids)
    
    @api.model
    def create(self, vals):
        # Code before create: should use the `vals` dict
        if 'stage_id' in vals:
            Stage = self.env['library.checkout.stage']
            new_state = Stage.browse(vals['stage_id']).state
            if new_state == 'open':
                vals['checkout_date'] = fields.Date.today()
        new_record = super().create(vals)
        # Code after create: can use the `new_record` created
        if new_record.state == 'done':
            raise exceptions.UserError(
                'Not allowed to create a checkout in the done state.')
        return new_record
    #修改记录
    @api.multi
    def write(self, vals):
        # Code before write: can use `self`, with the old values
        if 'stage_id' in vals:
            Stage = self.env['library.checkout.stage']
            new_state = Stage.browse(vals['stage_id']).state
            if new_state == 'open' and self.state != 'open':
                vals['checkout_date'] = fields.Date.today()
            if new_state == 'done' and self.state != 'done':
                vals['closed_date'] = fields.Date.today()
        super().write(vals)
        # Code after write: can use `self`, with the updated values
        return True

    @api.model
    def _default_stage(self):
        Stage = self.env['library.checkout.stage']
        return Stage.search([],limit=1)

    @api.model
    def _group_expand_stage_id(self,stages,domain,order):
        return stages.search([],order=order)

    stage_id = fields.Many2one(
        'library.checkout.stage',
        default=_default_stage,
        _group_expand='_group_expand_stage_id')
    state = fields.Selection(related='stage_id.state')

    @api.onchange('member_id')#onchange由用户表单视图触发，当用户编辑指定字段是，立即执行一段业务逻辑，用于执行验证
    def onchange_member_id(self):
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = fields.Date.today()
            return {
                'warning':{
                    'title': 'Changed Request Date',
                    'message': 'Request date changed to today.'
                }
            }


class CheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _rec_name = 'book_id'
    _description = 'Borrow Request Line'
    book_id = fields.Many2one('library.book')
    checkout_id = fields.Many2one('library.checkout')
    
