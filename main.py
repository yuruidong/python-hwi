#-*- coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define,options
define("port", default=8000, help="run on the given port", type=int)

SSO = False  # 是否启用单点登录
BACKCALL_URL = "http://host.sso/login?callback=http://localhost/index"  # SSO回调地址

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", user=self.current_user)


class LoginHandler(BaseHandler):
    def get(self):
        if SSO is True:
            try:
                username = self.get_argument("t")  # SSO返回token
            except SyntaxError:
                pass
            if username:
                self.set_secure_cookie("username", username)
                self.redirect("/")
            else:
                self.redirect(BACKCALL_URL)
        else:
            self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/")


class LoginoutHandler(BaseHandler):
    def get(self):
        if self.get_argument("loginout", None):
            self.clear_cookie("username")
            self.redirect("/")


if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "python_hwi_secret",
        "xsrf_cookies": False,
        "login_url": "/login"
    }

    app = tornado.web.Application([(r"/login", LoginHandler),
                                   (r"/loginout", LoginoutHandler),
                                   (r"/index", IndexHandler)], **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
