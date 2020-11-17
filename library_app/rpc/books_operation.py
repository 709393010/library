from xmlrpc import client

server_url = 'http://localhost:8888'
db_name = 'odoo12'
username = 'root'
password = '123456'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name,username,password,{})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)


if user_id:
    
    #create
    create_data = [
        {'name' : 'Book 1','date_published' : '2020-11-11'},
        {'name' : 'Book 2','date_published' : '2020-11-12'},
        {'name' : 'Book 3','date_published' : '2020-11-13'},
        {'name' : 'Book 4','date_published' : '2020-11-14'}
    ]

    book_ids = models.execute_kw(db_name,user_id,password,'library.book','create',[create_data])
    print("Books created:",book_ids)

    # #write
    book_to_write = book_ids[2]
    write_data = {'name' : 'Book 22'}
    written = models.execute_kw(db_name,user_id,password,'library.book','write',[book_to_write,write_data])
    print("Books written:",written)

    #delete
    book_to_delete = [69,70]
    deleted = models.execute_kw(db_name,user_id,password,'library.book','unlink',[book_to_delete])
    print('Books unlinked:',deleted)

    #select
    search_domain = ['&',['name','ilike','三'],['name','ilike','国']]
    book_ids = models.execute_kw(db_name,user_id,password,'library.book','search_read',[search_domain,['name','date_published']])
    print('Books ids found:' , book_ids)
else:
    print('Wrong credentials')


