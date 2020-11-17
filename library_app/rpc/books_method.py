from xmlrpc import client

server_url = 'http://localhost:8888'
db_name = 'odoo12'
username = 'root'
password = '123456'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name,username,password,{})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)


if user_id:
    #检查是否有创建图书的权限
    has_access = models.execute_kw(db_name, user_id, password,'library.book', 'check_access_rights',
        ['create'], {'raise_exception': False})
    print('Has create access on book:', has_access )

    # book_id = models.execute_kw(db_name, user_id, password,'library.book', 'create',
    #     [{'name':'New Book 2','date_published':'2019-01-01'}])
    models.execute_kw(db_name,user_id,password,'library.book','make_available',[[82]])

    book_data = models.execute_kw(db_name,user_id,password,'library.book','read',[[82],['name','state']])
    print('Book state after method call:',book_data[0]['state'])
    
else:
    print('Wrong credentials')


