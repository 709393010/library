
from odoo import api, fields, models
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError
from datetime import timedelta

# Odoo保留字段
# name(Char) -- _rec_name的默认值，在需要用来展示的时候使用
# active(Boolean) -- 设置记录的全局可见性，当值为False时通过search和list是获取不到的
# sequence(Integer) -- 可修改的排序，可以在列表视图里通过拖拽进行排序
# state(Selection) -- 对象的生命周期阶段，通过fileds的states属性使用
# parent_id(Many2one) -- 用来对树形结构的记录排序，并激活domain表达式的child_of运算符
# parent_left,parent_right -- 与 _parent_store结合使用，提供更好的树形结构数据读取

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _order= 'name, date_published asc'
    _sql_constraints =[ #数据库约束，保证name唯一
        ('name_uniq',
        'UNIQUE(name)',
        'Book title must be unique.')
    ]
    
    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    book_type = fields.Selection(
        [('paper', 'Paperback'),
        ('hard', 'Hardcover'),
        ('electronic', 'Electronic'),
        ('other', 'Other')],
        'Type')
    notes = fields.Text('Internal Notes')
    descr = fields.Html('Description')
     # Numeric fields:
    copies = fields.Integer(default=1)
    avg_rating = fields.Float('Average Rating', (3,2))
    price = fields.Monetary('Price', 'currency_id')
    currency_id = fields.Many2one('res.currency') # price helper
    last_borrow_date = fields.Datetime(
        'Last Borrowed On',
        default=lambda self: fields.Datetime.now())
    ###
    active = fields.Boolean('Active?', default=True)
    date_published = fields.Date('Published Date')
    image = fields.Binary('Cover')
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    #related 引用类型，由当前模型的某个关联字段的某个字段带出值
    publisher_city = fields.Char('Publisher City',related='publisher_id.city',readonly=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    category_id = fields.Many2one('library.book.category')
    date_updated = fields.Datetime('Date Update Time')
    
    #查找res.currency的id
    def default_currency_id(self):
        return self.env['res.currency'].search([])[0].id
    #添加货币字段
    currency_id = fields.Many2one('res.currency',string='Currency',
        default=default_currency_id)
    cost_price = fields.Monetary('Book Cost') #Monetary存储某个币种的数量值
    age_days = fields.Float(
         string='Days Since Publish',
         compute='_compute_age',
         inverse='_inverse_age',
         search='_search_age',
         store=False, # optional
         compute_sudo=False )
    #reference是比related更高级的引用字段，可以指定该字段引用那些模型范围内的模型的哪些字段的值，范围更广
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')
    html_description = fields.Html()

    #修改货币类型
    def	change_currency_id(self):
        self.currency_id = self.env['res.currency'].search([])[0].id

    #模拟丢失图书，并不改变图书真正的状态
    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'
        if not self.env.context.get('avoid_deactivate'):
            self.active = False 
    
   

    #更改执⾏动作的⽤户,让普通用户可以借书
    def book_rent(self):
        self.ensure_one()

        # if self.state != 'available' :
        #     raise UserError(_('Book is not available for renting'))

        #使⽤超级⽤户来获取library.book.rent的空记录集
        rent_as_superuser = self.env['library.book.rent'].sudo()
        rent_as_superuser.create({
            'book_id' : self.id,
            'borrower_id' : self.env.user.partner_id.id,
        })

    #更新模块时，自动增加图书的价格
    @api.model
    def update_book_price(self,increase):
        all_books = self.search([])
        for book in all_books:
            book.cost_price += increase

    #获取数据，计算每个分类的平均成本
    def get_average_cost(self): #button触发,在终端查看
        # import pdb  #加断点
        # pdb.set_trace()
        vals = self._get_average_cost()
        print(vals)
        return vals
    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price',"!=",False)],
            ['category_id','cost_price:avg'],
            ['category_id']
        )
        return grouped_result

    #更新date_updated字段
    @api.multi
    def change_update_date(self):
        self.ensure_one()
        self.date_updated = fields.Datetime.now()


    #计算图书发行时间
    @api.depends('date_published')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_published'):
            delta = today - book.date_published
            book.age_days = delta.days
    #实现客⼊计算字段的逻辑
    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_published'):
            d = today - timedelta(days=book.age_days)
            book.date_published = d
    #实现允许你在计算字段中进⾏搜索的逻辑
    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_published', new_op, value_date)]
        
    #使⽤引⽤字段添加动态关联,添加⼀个帮助⽅法来运⾏构建⼀个可选⽬标模型列表
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search(
            [('field_id.name','=','message_ids')] )
        return [(x.model,x.name) for x in models]

    #添加一个python约束，来防⽌使⽤未来的⽇期作为发⾏⽇期。
    @api.constrains('date_published')
    def _check_date_published(self):
        for record in self:
            if record.date_published and record.date_published > fields.Date.today():
                raise models.ValidationError('Publish date must be in the past')
    

    #搜索图书会员
    def get_all_library_member(self):
        vals = self._get_all_library_member()
        print (vals)
        #return vals
    @api.model
    def _get_all_library_member(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        isbn = self.isbn.replace('_','')
        digits = [int(x) for x in isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a,b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain !=0 else 0
            return digits[-1] == check

    @api.multi
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
            return True
    # 检查isbn是否合法
    @api.constrains('isbn')
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError('%s is an invalid ISBN' % book.isbn)
  
