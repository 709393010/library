from odoo import fields,models

class Partner(models.Model):
    _inherit = 'res.partner'
    published_book_ids = fields.One2many(
        'library.book', #关联模型
        'publisher_id', #引用该记录的模型字段
        string='Published Books')#字段标签
    book_ids = fields.Many2many(
        'library.book',
        string='Authored Books')