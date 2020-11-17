import odoorpc
db_name = 'odoo12'
user_name = 'root'
password = '123456'

odoo = odoorpc.ODOO('localhost',port=8888)
odoo.login(db_name,user_name,password)

user = odoo.env.user
print(user_name)
print(user.company_id.name)
print(user.email)

BookModel = odoo.env['library.book']
search_domain = [['name','ilike','三']]
books_ids = BookModel.search(search_domain,limit = 5)
for book in BookModel.browse(books_ids):
    print(book.name,book.date_published)

#create
# book_id = BookModel.create({'name' : 'Test book','state' : 'draft'})
# book = BookModel.browse(book_id)
# print("Book state before make_available:",book.state)
# book.make_available()
# book = BookModel.browse(book_id)
# print("Book state before make_available:",book.state)

book_search = BookModel.search([])
print('Book search:',book_search)

#write
BookModel.browse(1).write({'cost_price' : '68','age_days' : '15'})
book = BookModel.browse(1)
print('Book cost : ',book[0].cost_price,book[0].age_days)

#delete
book_del = BookModel.unlink(82)
print("Book del:",book_del)
