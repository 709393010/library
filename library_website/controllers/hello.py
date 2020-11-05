from odoo import http
from odoo.http import request

class Hello(http.Controller):
    @http.route('/helloworld',auto="public",website=True)
    def helloworld(self,**kwargs):
        return http.request.render('library_website.helloworld')