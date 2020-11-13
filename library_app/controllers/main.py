from odoo import http
from odoo.http import request
class Books(http.Controller):
    
    @http.route('/library/books',auth='user')
    def list(self, **kwargs):
        Book = http.request.env['library.book']
        books = Book.search([])
        return http.request.render(
            'library_app.book_list_template',{'books':books})
    
    #显示所有图书名，由当前用户所写的书加粗
    @http.route('/library/all_books',type='http',auth='public')
    def all_books(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            if request.env.user.partner_id.id in book.author_ids.ids:
               html_result += "<li> <b> %s </b> </li>" % book.name 
            else:
                html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    #通过book_id查书    
    @http.route('/library/book_details', type='http',auth="none")
    def book_details(self,book_id):
        record = request.env['library.book'].sudo().browse(int(book_id))
        return '<h1>%s</h1>Authors: %s' % (record.name,
            ','.join(record.author_ids.mapped('name')) or 'none')

    #添加⼀个我们可以传递图书ID的路径
    # @http.route("/library/book_details/<model('library.book'):book>",type='http',auth='none')
    # def book_details_in_path(self,book):
    #     return self.book_details(book.id)


    #图书详情页
    #url:    http://localhost:8888/books/1

    @http.route('/books/<model("library.book"):book>', type='http', auth="user", website=True)
    def library_book_detail(self,book):
        return request.render(
            'library_app.book_details',{
                'book' : book,
            }
        )