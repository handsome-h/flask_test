from flask import Flask

app = Flask(__name__)

# =================== 绑定路由 ====================
# Flask的URL规则基于Werkzeug的路由模块。
# 方式一： 采用装饰器方式，@app.route('/')，实际装饰器内也调用的是方式二
# 方式二：代用 add_url_rule()，app.add_url_rule('/', 'hello', hello_world)
@app.route('/')
def hello_world():
    return 'Hello World'
# 使用 /python 或 /python/返回相同的输出。如果不带后面的/，访问 /python/会返回404
@app.route('/python/')
def hello_python():
   return 'Hello Python'


# ================== 路径参数 =========================
@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name
@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID
@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo


# ======================== url构建 ======================
# url_for()函数对于动态构建特定函数的URL非常有用。
from flask import redirect, url_for
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'
@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest
@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest', guest=name))


# ======================= POST 请求 =========================
from flask import request
@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      print(1)
      user = request.form['nm']
      return redirect(url_for('success', name=user))
   else:
      print(2)
      user = request.args.get('nm')
      return redirect(url_for('success', name=user))


# ========================= 渲染模板 ===============================
# 视图函数作用：1、处理业务逻辑；2、返回响应内容；
# 在大型应用中,把业务逻辑和表现内容放在一起,会增加代码的复杂度和维护成本.
    # 模板其实是一个包含响应文本的文件,其中用占位符(变量)表示动态部分,告诉模板引擎其具体的值需要从使用的数据中获取
    # 使用真实值替换变量,再返回最终得到的字符串,这个过程称为'渲染'
    # Flask 是使用 Jinja2 这个模板引擎来渲染模板
# 使用模板的好处
    # 视图函数只负责业务逻辑和数据处理(业务逻辑方面)
    # 而模板则取到视图函数的数据结果进行展示(视图展示方面)
    # 代码结构清晰,耦合度低

# 在项目下创建 templates 文件夹，用于存放所有模板文件
from flask import render_template
# 向模板传递变量
@app.route('/hello_template')
def index():
    # 往模板中传入的数据
    my_str = 'Hello Word'
    my_int = 10
    my_array = [3, 4, 2, 1, 7, 9]
    my_dict = {
        'name': 'xiaoming',
        'age': 18
    }
    return render_template('hello.html',
                           my_str=my_str,
                           my_int=my_int,
                           my_array=my_array,
                           my_dict=my_dict
                           )



# ============================ 静态文件 ========================
@app.route("/test_static")
def test_static():
   return render_template("static.html")


# ============================ Request对象 ==========================
# Request对象的重要属性如下所列：
    # Form - 它是一个字典对象，包含表单参数及其值的键和值对。
    # args - 解析查询字符串的内容，它是问号（？）之后的URL的一部分。
    # Cookies  - 保存Cookie名称和值的字典对象。
    # files - 与上传文件有关的数据。
    # method - 当前请求方法。


# =========================== Cookie ==============================
from flask import make_response
@app.route("/set_cookies")
def set_cookie():
    """
    设置cookie，默认有效期是临时cookie,浏览器关闭就失效
    可以通过 max_age 设置有效期， 单位是秒
    :return:
    """
    resp = make_response("success")
    resp.set_cookie("cookie_name", "cookie_value", max_age=3600)
    return resp

@app.route("/get_cookies")
def get_cookie():
    cookie_1 = request.cookies.get("cookie_name")
    return cookie_1

@app.route("/delete_cookies")
def delete_cookie():
    """
    删除cookie，删除只是让cookie过期，并不是直接删除cookie
    :return:
    """
    resp = make_response("del success")
    resp.delete_cookie("cookie_name")

    return resp



# =============================== Session ===============================
# 与Cookie不同，Session（会话）数据存储在服务器上。会话是客户端登录到服务器并注销服务器的时间间隔。需要在该会话中保存的数据会存储在服务器上的临时目录中。
# 为每个客户端的会话分配会话ID。会话数据存储在cookie的顶部，服务器以加密方式对其进行签名。对于此加密，Flask应用程序需要一个定义的SECRET_KEY。
# Session对象也是一个字典对象，包含会话变量和关联值的键值对。
from flask import session, redirect, url_for, request

app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'

@app.route('/session/index')
def session_index():
    if 'username' in session:
        username = session['username']
        return '登录用户名是:' + username + '<br>' + "<b><a href = '/session/logout'>点击这里注销</a></b>"

    return "您暂未登录， <br><a href = '/session/login'></b>" + "点击这里登录</b></a>"
@app.route('/session/login', methods = ['GET', 'POST'])
def session_login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('session_index'))
    return '''
   <form action = "" method = "post">
      <p><input type="text" name="username"/></p>
      <p><input type="submit" value ="登录"/></p>
   </form>
   '''
@app.route('/session/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('session_index'))



# =========================== 重定向 ==========================
# redirect(location, statuscode, response)
    # location参数是应该重定向响应的URL。
    # statuscode发送到浏览器标头，默认为302。
    # response参数用于实例化响应。
@app.route('/redirect')
def redirect_index():
    return render_template('log_in.html')
@app.route('/redirect/login', methods=['POST', 'GET'])
def redirect_login():
    if request.method == 'POST' and request.form['username'] == 'admin':
        return redirect(url_for('success'))
    return redirect(url_for('index'))
@app.route('/redirect/success')
def redirect_success():
    return 'logged in successfully'




# ========================= 错误处理 ======================
# abort(code)
# 400 - 用于错误请求
# 401 - 用于未身份验证的
# 403 - Forbidden
# 404 - 未找到
# 406 - 表示不接受
# 415 - 用于不支持的媒体类型
# 429 - 请求过多
from flask import abort
@app.route('/error')
def error_index():
   return render_template('log_in.html')
@app.route('/error/login',methods = ['POST', 'GET'])
def error_login():
   if request.method == 'POST':
      if request.form['username'] == 'admin':
         return redirect(url_for('error_success'))
      else:
         abort(401)
   else:
      return redirect(url_for('error_index'))

@app.route('/error/success')
def error_success():
   return 'logged in successfully'



# ================================ 消息闪现 =================================
# 闪现系统使得在一个请求结束的时候记录一个信息，并且在下次（且仅在下一次中）请求时访问它，这通常与布局模板结合使用以公开信息。
# 在 Flask Web 应用程序中生成这样的信息性消息很容易。Flask 框架的闪现系统可以在一个视图中创建消息，并在名为 next 的视图函数中呈现它。
# Flask 模块包含 flash() 方法。它将消息传递给下一个请求，该请求通常是一个模板。
# flash(message, category)
    # message 参数是要闪现的实际消息。
    # category 参数是可选的。它可以是“error”，“info”或“warning”。
# 为了从会话中删除消息，模板调用 get_flashed_messages()。
    # get_flashed_messages(with_categories, category_filter)，两个参数都是可选的。如果接收到的消息具有类别，则第一个参数是元组。第二个参数仅用于显示特定消息。

# https://www.w3cschool.cn/flask/flask_message_flashing.html


#  ============================ 文件上传 ======================================
# 在 Flask 中处理文件上传非常简单。它需要一个 HTML 表单，其 enctype 属性设置为“multipart/form-data”，将文件发布到 URL。
# URL 处理程序从 request.files[] 对象中提取文件，并将其保存到所需的位置。
# 每个上传的文件首先会保存在服务器上的临时位置，然后将其实际保存到它的最终位置。
# 目标文件的名称可以是硬编码的，也可以从 request.files[file] 对象的 filename 属性中获取。
# 但是，建议使用 secure_filename() 函数获取它的安全版本。

# 可以在 Flask 对象的配置设置中定义默认上传文件夹的路径和上传文件的最大大小。
# app.config['UPLOAD_FOLDER'] 定义上传文件夹的路径
# app.config['MAX_CONTENT_LENGTH'] 指定要上传的文件的最大大小（以字节为单位）

import os
from werkzeug.utils import secure_filename
app.config['UPLOAD_FOLDER'] = 'upload/'
@app.route('/upload')
def upload_file():
    return render_template('upload.html')
@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        return 'file uploaded successfully'

    else:
        return render_template('upload.html')



# =================================== 扩展 ===============================
# Flask通常被称为微框架，因为核心功能包括基于Werkzeug的WSGI和路由以及基于Jinja2的模板引擎。此外，Flask框架还支持cookie和会话，以及JSON，静态文件等Web帮助程序。
# Flask扩展为Flask框架提供了可扩展性。
# Flask扩展是一个Python模块，它向Flask应用程序添加了特定类型的支持。
# Flask Extension Registry（Flask扩展注册表）是一个可用的扩展目录。
# 可以通过pip实用程序下载所需的扩展名。

# Flask常用扩展包：
# Flask-SQLalchemy：操作数据库；
# Flask-script：插入脚本；
# Flask-migrate：管理迁移数据库；
# Flask-Session：Session存储方式指定；
# Flask-WTF：表单；
# Flask-Mail：邮件；
# Flask-Bable：提供国际化和本地化支持，翻译；
# Flask-Login：认证用户状态；
# Flask-OpenID：认证；
# Flask-RESTful：开发REST API的工具；
# Flask-Bootstrap：集成前端Twitter Bootstrap框架；
# Flask-Moment：本地化日期和时间；
# Flask-Admin：简单而可扩展的管理接口的框架

# Flask 的扩展通常命名为“ Flask-Foo ”或者“ Foo-Flask ” 。可以在 PyPI 搜索 标记为 Framework :: Flask 扩展包。



# ===================================== 部署 ====================================
# 方式一：Apache部署
# 方式二：python web服务器，如 Gunicorn、Tornado



# ==================================== 即插视图 =================================
# 略，参考：https://www.w3cschool.cn/flask/flask-9e2a3gdn.html


# ==================================== 应用上下文 =================================
# Flask 背后的设计理念之一就是，代码在执行时会处于两种不同的“状态”（states）。 当Flask对象被实例化后在模块层次上应用便开始隐式地处于应用配置状态。
# 一直到第一个请求到达，这种状态才隐式地结束。当应用处于这个状态的时候 ，你可以认为下面的假设是成立的
    # 程序员可以安全地修改应用对象
    # 目前还没有处理任何请求
    # 你必须得有一个指向应用对象的引用来修改它。不会有某个神奇的代理变量指向 你刚创建的或者正在修改的应用对象的
# 相反，到了第二个状态，在处理请求时，有一些其它的规则:
    # 当一个请求激活时，上下文的本地对象（ flask.request和其它对象等） 指向当前的请求
    # 你可以在任何时间里使用任何代码与这些对象通信

# 作用
# 应用上下文存在的主要原因是，在过去，请求上下文被附加了一堆函数，但是又没 有什么好的解决方案。
# 因为 Flask 设计的支柱之一是你可以在一个 Python 进程中 拥有多个应用。
# 那么代码如何找到“正确的”应用？
# 在过去，我们推荐显式地到处传递应用，但是这 会让我们在使用不是以这种理念设计的库时遇到问题。
# 解决上述问题的常用方法是使用后面将会提到的 current_app 代 理对象，它被绑定到当前请求的应用的引用。
# 既然无论如何在没有请求时创建一个 这样的请求上下文是一个没有必要的昂贵操作，应用上下文就被引入了。

# 创建
# 有两种方式来创建应用上下文。
# 第一种是隐式的：无论何时当一个请求上下文被压栈时， 如果有必要的话一个应用上下文会被一起创建。 由于这个原因，你可以忽略应用 上下文的存在，除非你需要它。
# 第二种是显式地调用 app_context() 方法:
from flask import current_app
with app.app_context():
    print(current_app.name)
# 在配置了 SERVER_NAME 时，应用上下文也被用于 url_for() 函 数。这允许你在没有请求时生成 URL 。



# ================================= 请求上下文 ===========================

# 创建请求上下文
ctx = app.test_request_context('/?next=http://example.com/')
# 可以通过两种方式利用这个上下文：使用 with 声明或是调用 push() 和 pop() 方法:
ctx.push()  # 从这点开始，你可以使用请求对象
ctx.pop()  # 从这点开始，请求对象不再可用
# 因为请求上下文在内部作为一个栈来维护，所以你可以多次压栈出栈。这在实现 内部重定向之类的东西时很方便。

# 请求上下文内部工作如同一个栈。栈顶是当前活动的请求。 push() 把上下文添加到栈顶， pop() 把它移出栈。在出栈时，应用的 teardown_request() 函数也会被执行。
# 另一件需要注意的事是，请求上下文被压入栈时，并且没有当前应用的应用上下文， 它会自动创建一个 应用上下文 。


# 请求响应执行过程
# 在每个请求之前，执行 before_request() 上绑定的函数。 如果这些函数中的某个返回了一个响应，其它的函数将不再被调用。任何情况 下，无论如何这个返回值都会替换视图的返回值。
# 如果 before_request() 上绑定的函数没有返回一个响应， 常规的请求处理将会生效，匹配的视图函数有机会返回一个响应。
# 视图的返回值之后会被转换成一个实际的响应对象，并交给 after_request() 上绑定的函数适当地替换或修改它。
# 在请求的最后，会执行 teardown_request() 上绑定的函 数。这总会发生，即使在一个未处理的异常抛出后或是没有请求前处理器执行过 （例如在测试环境中你有时会想不执行请求前回调）。




# ======================================== 蓝图 blueprints =======================================
# 蓝图 在一个应用中或跨应用制作应用组件和支持通用的模式。
# 蓝图很好地简化了大型应用工作的方式，并提供给 Flask 扩展在应用 上注册操作的核心方法。
# 一个 Blueprint 对象与 Flask 应用对象的工作方式很像，但它确实不是一个应用，而是一个描述如何构建或扩展应用的 蓝图 。

# Flask 中的蓝图为这些情况设计:
    # 把一个应用分解为一个蓝图的集合。这对大型应用是理想的。一个项目可以实例化 一个应用对象，初始化几个扩展，并注册一集合的蓝图。
    # 以 URL 前缀和/或子域名，在应用上注册一个蓝图。 URL 前缀/子域名中的参数即 成为这个蓝图下的所有视图函数的共同的视图参数（默认情况下）。
    # 在一个应用中用不同的 URL 规则多次注册一个蓝图。
    # 通过蓝图提供模板过滤器、静态文件、模板和其它功能。一个蓝图不一定要实现应 用或者视图函数。
    # 初始化一个 Flask 扩展时，在这些情况中注册一个蓝图。

# Flask 中的蓝图不是即插应用，因为它实际上并不是一个应用——它是可以注册，甚至 可以多次注册到应用上的操作集合。为什么不使用多个应用对象？你可以做到那样 （见 应用调度 ），但是你的应用的配置是分开的，并在 WSGI 层管理。
# 蓝图作为 Flask 层提供分割的替代，共享应用配置，并且在必要情况下可以更改所 注册的应用对象。它的缺点是你不能在应用创建后撤销注册一个蓝图而不销毁整个 应用对象。

# 蓝图的基本设想是当它们注册到应用上时，它们记录将会被执行的操作。 当分派请求和生成从一个端点到另一个的 URL 时，Flask 会关联蓝图中的视图函数。

# 注册蓝图
from apps.app01 import simple_page
app.register_blueprint(simple_page)
# app.register_blueprint(simple_page, url_prefix='/pages')



# ======================================== 中间件 ================================
# 请求执行之前的顺序是:谁先注册，谁就先执行
# 注意：如果before_request中有返回值，那后面的before就不会执行，且响应函数也不会执行
#         但是after_request任然会全部执行（这里与django不同，django是同级返回）
@app.before_request
def before_req1(*args, **kwargs):
    # 如果是login,可以通过白名单
    if request.path == '/login':
        return None
    user = session.get('user_info')
    if user:
        return None
    return redirect("/login")
    print("请求之前")

@app.before_request
def before_req2(*args, **kwargs):
    # 如果是login,可以通过白名单
    if request.path == '/login':
        return None
    user = session.get('user_info')
    if user:
        return None
    return redirect("/login")
    print("请求之前")

# 响应函数之后执行，相当于django的process_response,在响应函数之后执行的。after_request的执行顺序是：先注册，后执行
#after_request必须接受一个参数，参数为response对象，且必须返回
@app.after_request
def process_response1(response):
    # 返回值存在
    print("process_response1走了")
    return response




# 在执行app.run()方法的时候，最终执行run_simple，最后执行app()，也就是执行app.__call__方法。
# 在app.__call__里面，执行的是self.wsgi_app()，那么我们希望在执行它本身的wsgi_app之前或者之后做点事情。这就是中间件的应用
# 中间件类
class MyMiddleware:
    def __init__(self,wsgi_app):
        self.wsgi_app = wsgi_app
    def __call__(self, environ, start_response):
        print('我是开始之前')
        res = self.wsgi_app(environ, start_response)
        print('我是所有之后')
        return res

# app.wsgi_app = MyMiddleware(app.wsgi_app)
# app.run()






if __name__ == '__main__':
    # Flask类的run()方法在本地开发服务器上运行应用程序。
    # app.run(host, port, debug, options)
    # host 要监听的主机名。 默认为127.0.0.1（localhost）。设置为“0.0.0.0”以使服务器在外部可用
    # post 默认值为5000
    # debug 默认为false。 如果设置为true，则提供调试信息。 两种方式设置方式一 app.debug=True；方式二 app.run(debug = True)；
    # options 要转发到底层的Werkzeug服务器。
    app.run()
