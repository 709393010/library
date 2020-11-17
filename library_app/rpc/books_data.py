from xmlrpc import client
server_url = 'http://localhost:8888'
db_name = 'odoo12'
username = 'root'
password = '123456'
common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)
version_info = common.version()
print(version_info)
if user_id:
  search_domain = ['|', ['name', 'ilike', '三'], ['name', 'ilike', 'test']]
  books_ids = models.execute_kw(db_name, user_id, password,'library.book', 'search_read',
    [search_domain,['name','date_published']],{'limit': 5})
  print('Books ids found:', books_ids)
  # books_data = models.execute_kw(db_name, user_id, password,
  #   'library.book', 'read',
  #   [books_ids, ['name', 'date_published']])
  # print("Books data:", books_data)
else:
  print('Wrong credentials')


