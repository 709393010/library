from odoo import fields, models

class Member(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    #继承代理：基于已有模型新建一个模型来使用其已有的功能
    _inherits = {'res.partner' : 'partner_id'}
    
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
    card_number = fields.Char()
    partner_id = fields.Many2one(
        'res.partner',
        delegate=True,
        ondelete='cascade',
        required=True)
    # 使用mixin类继承模型
    _inherit = ['mail.thread','mail.activity.mixin']